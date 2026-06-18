#!/usr/bin/env python
"""
Invoke the lambda function directly (the CLI equivalent of the Test button)

Sends an empty event ({}) and prints the function's return value. Anything the
function prints goes to CloudWatch (see read_logs.py).
"""

import json

import boto3

FUNCTION_NAME = "mark-veltzer"
REGION = "us-east-1"

lam = boto3.client("lambda", region_name=REGION)
resp = lam.invoke(
    FunctionName=FUNCTION_NAME,
    Payload=json.dumps({}).encode(),
)

print(f"status code: {resp['StatusCode']}")
if "FunctionError" in resp:
    print(f"function error: {resp['FunctionError']}")
payload = resp["Payload"].read().decode()
print(f"response payload: {payload}")
