#!/usr/bin/env python
"""
Create a Standard SQS queue and open it to the entire world

The access policy below lets anyone (Principal "*") send, receive and delete
messages. This is intentionally insecure for the exercise - do NOT do this with
a real queue.
"""

import json

import boto3

QUEUE_NAME = "mark-veltzer"
REGION = "us-east-1"

sqs = boto3.client("sqs", region_name=REGION)
resp = sqs.create_queue(QueueName=QUEUE_NAME)
queue_url = resp["QueueUrl"]
print(f"created queue {QUEUE_NAME} -> {queue_url}")

# the policy needs the queue ARN, fetch it from the queue attributes
queue_arn = sqs.get_queue_attributes(
    QueueUrl=queue_url,
    AttributeNames=["QueueArn"],
)["Attributes"]["QueueArn"]

policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowEveryone",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "sqs:SendMessage",
                "sqs:ReceiveMessage",
                "sqs:DeleteMessage",
            ],
            "Resource": queue_arn,
        }
    ],
}

sqs.set_queue_attributes(
    QueueUrl=queue_url,
    Attributes={"Policy": json.dumps(policy)},
)
print("attached policy allowing everyone to send/receive/delete messages")
