from constructs import Construct


class StorageConstruct(Construct):
    """
    S3 bucket for resume and job description uploads.

    Excluded from Phase 2 — added once the backend upload flow is implemented.

    Planned resources:
    - S3 bucket (private, S3-managed encryption, versioning enabled)
    - Bucket policy restricting access to backend and worker task roles only
    - Lifecycle rule to expire temporary uploads after 7 days
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # TODO Phase 3+: implement S3 bucket
        # self.bucket = s3.Bucket(self, "AssetsBucket", ...)
