#!/bin/bash
# Runs automatically when LocalStack is ready.
# Creates the SQS queues and S3 bucket that the backend and worker expect.

set -e

AWS_CMD="aws --endpoint-url=http://localhost:4566 --region us-east-1"

echo "[init] Creating SQS dead-letter queue..."
$AWS_CMD sqs create-queue --queue-name zzuck-jobs-dlq

echo "[init] Creating SQS job queue..."
DLQ_ARN=$($AWS_CMD sqs get-queue-attributes \
  --queue-url http://localhost:4566/000000000000/zzuck-jobs-dlq \
  --attribute-names QueueArn \
  --query 'Attributes.QueueArn' \
  --output text)

$AWS_CMD sqs create-queue \
  --queue-name zzuck-jobs \
  --attributes "{
    \"VisibilityTimeout\": \"300\",
    \"RedrivePolicy\": \"{\\\"deadLetterTargetArn\\\":\\\"${DLQ_ARN}\\\",\\\"maxReceiveCount\\\":\\\"3\\\"}\"
  }"

echo "[init] Creating S3 bucket..."
$AWS_CMD s3 mb s3://zzuck-assets-local

echo "[init] LocalStack resources ready."
echo "[init]   SQS queue URL : http://localhost:4566/000000000000/zzuck-jobs"
echo "[init]   S3 bucket     : zzuck-assets-local"
