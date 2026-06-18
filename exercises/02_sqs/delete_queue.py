#!/usr/bin/env python
"""
Delete the SQS queue
"""

import boto3

QUEUE_NAME = "mark-veltzer"
REGION = "us-east-1"

sqs = boto3.client("sqs", region_name=REGION)
queue_url = sqs.get_queue_url(QueueName=QUEUE_NAME)["QueueUrl"]
sqs.delete_queue(QueueUrl=queue_url)
print(f"deleted queue {QUEUE_NAME}")
