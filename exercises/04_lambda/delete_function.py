#!/usr/bin/env python
"""
Delete everything this exercise created

Removes (ignoring "not found" so it is safe to run repeatedly):
  1. the lambda function
  2. the CloudWatch log group (deleting the function does not delete this)
  3. the IAM execution role (detaching its managed policies first)

Run remove_sqs_trigger.py before this if you did Phase II.
"""

import boto3

FUNCTION_NAME = "mark-veltzer"
ROLE_NAME = "mark-veltzer-lambda-role"
REGION = "us-east-1"
LOG_GROUP = f"/aws/lambda/{FUNCTION_NAME}"

lam = boto3.client("lambda", region_name=REGION)
logs = boto3.client("logs", region_name=REGION)
iam = boto3.client("iam", region_name=REGION)

# 1. the function
try:
    lam.delete_function(FunctionName=FUNCTION_NAME)
    print(f"deleted function {FUNCTION_NAME}")
except lam.exceptions.ResourceNotFoundException:
    print(f"function {FUNCTION_NAME} not found")

# 2. the log group
try:
    logs.delete_log_group(logGroupName=LOG_GROUP)
    print(f"deleted log group {LOG_GROUP}")
except logs.exceptions.ResourceNotFoundException:
    print(f"log group {LOG_GROUP} not found")

# 3. the role: detach managed policies, then delete it
try:
    attached = iam.list_attached_role_policies(RoleName=ROLE_NAME)[
        "AttachedPolicies"
    ]
    for policy in attached:
        iam.detach_role_policy(
            RoleName=ROLE_NAME, PolicyArn=policy["PolicyArn"]
        )
        print(f"detached {policy['PolicyName']}")
    iam.delete_role(RoleName=ROLE_NAME)
    print(f"deleted role {ROLE_NAME}")
except iam.exceptions.NoSuchEntityException:
    print(f"role {ROLE_NAME} not found")
