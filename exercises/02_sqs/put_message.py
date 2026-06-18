#!/usr/bin/env python
"""
Put a message into the SQS queue
"""

import boto3

QUEUE_NAME = "mark-veltzer"
REGION = "us-east-1"
MESSAGE = "hello, world!"

sqs = boto3.client("sqs", region_name=REGION)
queue_url = sqs.get_queue_url(QueueName=QUEUE_NAME)["QueueUrl"]
resp = sqs.send_message(QueueUrl=queue_url, MessageBody=MESSAGE)
print(f"sent message {resp['MessageId']} to {QUEUE_NAME}")
