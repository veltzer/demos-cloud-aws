#!/usr/bin/env python
"""
Read the function's CloudWatch logs

Lambda writes to the log group /aws/lambda/<function name>. This prints the most
recent log events so you can confirm the function ran and see "hello, world!".
"""

import boto3

FUNCTION_NAME = "mark-veltzer"
REGION = "us-east-1"
LOG_GROUP = f"/aws/lambda/{FUNCTION_NAME}"

logs = boto3.client("logs", region_name=REGION)

# find the newest log stream
streams = logs.describe_log_streams(
    logGroupName=LOG_GROUP,
    orderBy="LastEventTime",
    descending=True,
    limit=1,
)["logStreams"]

if not streams:
    print(f"no log streams yet in {LOG_GROUP} (has the function run?)")
    raise SystemExit

stream_name = streams[0]["logStreamName"]
print(f"reading {LOG_GROUP} -> {stream_name}\n")

events = logs.get_log_events(
    logGroupName=LOG_GROUP,
    logStreamName=stream_name,
    startFromHead=True,
)["events"]

for event in events:
    print(event["message"].rstrip())
