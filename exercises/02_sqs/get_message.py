#!/usr/bin/env python
"""
Get a message from the SQS queue and delete it after handling
"""

import boto3

QUEUE_NAME = "mark-veltzer"
REGION = "us-east-1"

sqs = boto3.client("sqs", region_name=REGION)
queue_url = sqs.get_queue_url(QueueName=QUEUE_NAME)["QueueUrl"]
resp = sqs.receive_message(QueueUrl=queue_url, WaitTimeSeconds=10)
messages = resp.get("Messages", [])
if not messages:
    print("no messages available (try again)")
for msg in messages:
    print(f"received: {msg['Body']}")
    # delete after handling, otherwise it reappears after the visibility timeout
    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=msg["ReceiptHandle"])
    print("deleted message from queue")
