import aws_cdk as cdk
from aws_cdk import (
    aws_ecr as ecr,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_logs as logs,
)
from constructs import Construct


class ComputeConstruct(Construct):
    """
    ECR repository, ECS Fargate cluster, and backend task definition with CloudWatch logging.

    Phase 2 scope: ECR + cluster + task definition only.
    No Fargate Service is created here — added in a later phase once RDS and SQS are ready.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc: ec2.Vpc,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ── ECR ──────────────────────────────────────────────────────────────
        self.backend_repo = ecr.Repository(
            self,
            "BackendRepo",
            repository_name="careeriq-backend",
            removal_policy=cdk.RemovalPolicy.RETAIN,
            lifecycle_rules=[
                # Keep only the 5 most recent images to limit storage cost.
                ecr.LifecycleRule(max_image_count=5),
            ],
        )

        # Future: worker ECR repo — added when worker service is deployed.
        # self.worker_repo = ecr.Repository(self, "WorkerRepo", ...)

        # ── ECS Cluster ──────────────────────────────────────────────────────
        self.cluster = ecs.Cluster(
            self,
            "Cluster",
            vpc=vpc,
            cluster_name="careeriq",
            container_insights=True,
        )

        # ── CloudWatch log group ──────────────────────────────────────────────
        self.log_group = logs.LogGroup(
            self,
            "BackendLogGroup",
            log_group_name="/ecs/careeriq-backend",
            retention=logs.RetentionDays.ONE_WEEK,
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        # ── Backend task definition ───────────────────────────────────────────
        self.backend_task_def = ecs.FargateTaskDefinition(
            self,
            "BackendTaskDef",
            memory_limit_mib=512,
            cpu=256,
        )

        self.backend_task_def.add_container(
            "BackendContainer",
            image=ecs.ContainerImage.from_ecr_repository(self.backend_repo, "latest"),
            port_mappings=[ecs.PortMapping(container_port=8000)],
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix="backend",
                log_group=self.log_group,
            ),
            # Environment variables for external integrations are injected here
            # once RDS, SQS, and S3 constructs are added in later phases.
            environment={},
        )

        # Future: worker task definition — added when worker service is deployed.
        # self.worker_task_def = ecs.FargateTaskDefinition(self, "WorkerTaskDef", ...)

        # Future: Fargate services (backend + worker) — added in Phase 3+.
        # Requires RDS endpoint, SQS queue URL, and S3 bucket name.
        # self.backend_service = ecs.FargateService(self, "BackendService", ...)
        # self.worker_service  = ecs.FargateService(self, "WorkerService", ...)
