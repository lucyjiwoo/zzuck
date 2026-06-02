from constructs import Construct


class MessagingConstruct(Construct):
    """
    SQS queue for async job processing (answer evaluation, question generation).

    Excluded from Phase 2 — added together with the worker service deployment.

    Planned resources:
    - SQS dead-letter queue (14-day retention)
    - SQS main job queue (visibility timeout 300s, max 3 retries before DLQ)
    - IAM grants: backend task role → send, worker task role → consume
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # TODO Phase 3+: implement SQS queues
        # self.dead_letter_queue = sqs.Queue(self, "JobDeadLetterQueue", ...)
        # self.job_queue = sqs.Queue(self, "JobQueue", ...)
