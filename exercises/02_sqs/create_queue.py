#!/usr/bin/env python
"""
Create a Standard SQS queue
"""

import boto3

QUEUE_NAME = "mark-veltzer"
REGION = "us-east-1"

sqs = boto3.client("sqs", region_name=REGION)
resp = sqs.create_queue(QueueName=QUEUE_NAME)
print(f"created queue {QUEUE_NAME} -> {resp['QueueUrl']}")
