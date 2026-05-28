import aws_cdk as cdk
from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecr as ecr,
    aws_rds as rds,
    aws_s3 as s3,
    aws_sqs as sqs,
)
from constructs import Construct


class ZzuckStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ─────────────────────────────────────────
        # VPC
        # ─────────────────────────────────────────
        vpc = ec2.Vpc(
            self,
            "VPC",
            availability_zones=["us-east-1a", "us-east-1b"],
            nat_gateways=1,
        )

        # ─────────────────────────────────────────
        # ECR — container image repositories
        # ─────────────────────────────────────────
        backend_repo = ecr.Repository(
            self,
            "BackendRepo",
            repository_name="zzuck-backend",
            removal_policy=cdk.RemovalPolicy.RETAIN,
        )

        worker_repo = ecr.Repository(
            self,
            "WorkerRepo",
            repository_name="zzuck-worker",
            removal_policy=cdk.RemovalPolicy.RETAIN,
        )

        # ─────────────────────────────────────────
        # S3 — resume and job description storage
        # ─────────────────────────────────────────
        assets_bucket = s3.Bucket(
            self,
            "AssetsBucket",
            bucket_name=f"zzuck-assets-{self.account}",
            removal_policy=cdk.RemovalPolicy.RETAIN,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
        )

        # ─────────────────────────────────────────
        # SQS — async job queue
        # ─────────────────────────────────────────
        dead_letter_queue = sqs.Queue(
            self,
            "JobDeadLetterQueue",
            queue_name="zzuck-jobs-dlq",
            retention_period=cdk.Duration.days(14),
        )

        job_queue = sqs.Queue(
            self,
            "JobQueue",
            queue_name="zzuck-jobs",
            visibility_timeout=cdk.Duration.seconds(300),
            dead_letter_queue=sqs.DeadLetterQueue(
                queue=dead_letter_queue,
                max_receive_count=3,
            ),
        )

        # ─────────────────────────────────────────
        # RDS — PostgreSQL with pgvector
        # ─────────────────────────────────────────
        database = rds.DatabaseInstance(
            self,
            "Database",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_16
            ),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.T3, ec2.InstanceSize.MICRO
            ),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
            ),
            credentials=rds.Credentials.from_generated_secret("zzuck_admin"),
            database_name="zzuck",
            removal_policy=cdk.RemovalPolicy.SNAPSHOT,
            deletion_protection=True,
        )

        # ─────────────────────────────────────────
        # ECS Cluster
        # ─────────────────────────────────────────
        cluster = ecs.Cluster(
            self,
            "Cluster",
            vpc=vpc,
            cluster_name="zzuck",
        )

        # ─────────────────────────────────────────
        # Backend task definition (stub)
        # Add a Fargate service when ready to deploy.
        # ─────────────────────────────────────────
        backend_task_def = ecs.FargateTaskDefinition(
            self,
            "BackendTaskDef",
            memory_limit_mib=512,
            cpu=256,
        )

        backend_task_def.add_container(
            "BackendContainer",
            image=ecs.ContainerImage.from_ecr_repository(backend_repo, "latest"),
            port_mappings=[ecs.PortMapping(container_port=8000)],
            logging=ecs.LogDrivers.aws_logs(stream_prefix="zzuck-backend"),
            environment={
                "POSTGRES_HOST": database.instance_endpoint.hostname,
                "POSTGRES_PORT": "5432",
                "POSTGRES_DB": "zzuck",
                "SQS_QUEUE_URL": job_queue.queue_url,
                "S3_BUCKET_NAME": assets_bucket.bucket_name,
            },
        )

        # ─────────────────────────────────────────
        # Worker task definition (stub)
        # ─────────────────────────────────────────
        worker_task_def = ecs.FargateTaskDefinition(
            self,
            "WorkerTaskDef",
            memory_limit_mib=512,
            cpu=256,
        )

        worker_task_def.add_container(
            "WorkerContainer",
            image=ecs.ContainerImage.from_ecr_repository(worker_repo, "latest"),
            logging=ecs.LogDrivers.aws_logs(stream_prefix="zzuck-worker"),
            environment={
                "POSTGRES_HOST": database.instance_endpoint.hostname,
                "POSTGRES_PORT": "5432",
                "POSTGRES_DB": "zzuck",
                "SQS_QUEUE_URL": job_queue.queue_url,
                "S3_BUCKET_NAME": assets_bucket.bucket_name,
            },
        )

        # ─────────────────────────────────────────
        # Grants
        # ─────────────────────────────────────────
        assets_bucket.grant_read_write(backend_task_def.task_role)
        assets_bucket.grant_read(worker_task_def.task_role)
        job_queue.grant_send_messages(backend_task_def.task_role)
        job_queue.grant_consume_messages(worker_task_def.task_role)

        # ─────────────────────────────────────────
        # Stack outputs
        # ─────────────────────────────────────────
        cdk.CfnOutput(self, "BackendRepoUri", value=backend_repo.repository_uri)
        cdk.CfnOutput(self, "WorkerRepoUri", value=worker_repo.repository_uri)
        cdk.CfnOutput(self, "JobQueueUrl", value=job_queue.queue_url)
        cdk.CfnOutput(self, "AssetsBucketName", value=assets_bucket.bucket_name)
        cdk.CfnOutput(self, "DatabaseEndpoint", value=database.instance_endpoint.hostname)
