#!/usr/bin/env python
"""
Phase II: trigger the lambda from the SQS queue (event source mapping)

Steps:
  1. give the execution role permission to read/delete from SQS
     (AWSLambdaSQSQueueExecutionRole grants exactly that)
  2. create an event source mapping from the queue to the function

After this, every message sent to the queue invokes the function and the
messages arrive in event["Records"]. SQS deletes them once the function returns
successfully, so you do not call delete_message yourself.
"""

import time

import boto3

FUNCTION_NAME = "mark-veltzer"
ROLE_NAME = "mark-veltzer-lambda-role"
QUEUE_NAME = "mark-veltzer"
REGION = "us-east-1"

iam = boto3.client("iam", region_name=REGION)
lam = boto3.client("lambda", region_name=REGION)
sqs = boto3.client("sqs", region_name=REGION)

# 1. let the execution role read from the queue
iam.attach_role_policy(
    RoleName=ROLE_NAME,
    PolicyArn="arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole",
)
print("attached AWSLambdaSQSQueueExecutionRole (read from SQS)")
print("waiting for the policy to propagate ...")
time.sleep(10)

# 2. find the queue ARN and wire it up as a trigger
queue_url = sqs.get_queue_url(QueueName=QUEUE_NAME)["QueueUrl"]
queue_arn = sqs.get_queue_attributes(
    QueueUrl=queue_url,
    AttributeNames=["QueueArn"],
)["Attributes"]["QueueArn"]

resp = lam.create_event_source_mapping(
    EventSourceArn=queue_arn,
    FunctionName=FUNCTION_NAME,
    BatchSize=10,
    Enabled=True,
)
print(f"created event source mapping {resp['UUID']}")
print(f"  {queue_arn} -> {FUNCTION_NAME}")
