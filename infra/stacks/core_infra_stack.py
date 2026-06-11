import aws_cdk as cdk
from constructs import Construct

from infra_components.networking import NetworkingConstruct
from infra_components.compute import ComputeConstruct

# Future imports — uncomment as each phase is implemented:
# from infra_components.storage import StorageConstruct
# from infra_components.database import DatabaseConstruct
# from infra_components.messaging import MessagingConstruct


class CareerIQStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ── Phase 2 ───────────────────────────────────────────────────────────

        networking = NetworkingConstruct(self, "Networking")

        compute = ComputeConstruct(self, "Compute", vpc=networking.vpc)

        # ── Future phases ─────────────────────────────────────────────────────

        # Phase 3: storage = StorageConstruct(self, "Storage")
        # Phase 3: database = DatabaseConstruct(self, "Database", vpc=networking.vpc)
        # Phase 3: messaging = MessagingConstruct(self, "Messaging")

        # Phase 3: wire env vars into compute containers once deps are ready
        # Phase 3: grant compute.backend_task_def.task_role -> storage, messaging
        # Phase 3: grant compute.worker_task_def.task_role  -> storage, messaging

        # ── Outputs ───────────────────────────────────────────────────────────

        cdk.CfnOutput(
            self,
            "BackendRepoUri",
            value=compute.backend_repo.repository_uri,
            description="ECR URI for the backend image",
        )

        cdk.CfnOutput(
            self,
            "EcsClusterName",
            value=compute.cluster.cluster_name,
            description="ECS cluster name",
        )

        cdk.CfnOutput(
            self,
            "BackendLogGroupName",
            value=compute.log_group.log_group_name,
            description="CloudWatch log group for the backend service",
        )
