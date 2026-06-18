#!/usr/bin/env python
"""
Create the lambda function (and its execution role)

Steps:
  1. create an IAM execution role the function assumes when it runs
  2. attach AWSLambdaBasicExecutionRole so it can write logs to CloudWatch
  3. zip lambda_function.py (the .py must sit at the top level of the zip)
  4. create the function with that code and role

Re-running is safe: the role/function are reused if they already exist.
"""

import io
import json
import time
import zipfile

import boto3

FUNCTION_NAME = "mark-veltzer"
ROLE_NAME = "mark-veltzer-lambda-role"
REGION = "us-east-1"
RUNTIME = "python3.12"
HANDLER = "lambda_function.handler"
SOURCE_FILE = "lambda_function.py"

iam = boto3.client("iam", region_name=REGION)
lam = boto3.client("lambda", region_name=REGION)

# 1. trust policy: allow the lambda service to assume this role
trust_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole",
        }
    ],
}

try:
    role = iam.create_role(
        RoleName=ROLE_NAME,
        AssumeRolePolicyDocument=json.dumps(trust_policy),
        Description="execution role for the lambda exercise",
    )
    role_arn = role["Role"]["Arn"]
    print(f"created role {ROLE_NAME} -> {role_arn}")
except iam.exceptions.EntityAlreadyExistsException:
    role_arn = iam.get_role(RoleName=ROLE_NAME)["Role"]["Arn"]
    print(f"role {ROLE_NAME} already exists -> {role_arn}")

# 2. let the function write logs to CloudWatch
iam.attach_role_policy(
    RoleName=ROLE_NAME,
    PolicyArn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
)
print("attached AWSLambdaBasicExecutionRole (CloudWatch logs)")

# a freshly created role takes a few seconds to become usable by lambda
print("waiting for the role to propagate ...")
time.sleep(10)

# 3. zip the source in memory, with the .py at the top level of the zip
buf = io.BytesIO()
with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
    zf.write(SOURCE_FILE, arcname=SOURCE_FILE)
zip_bytes = buf.getvalue()

# 4. create (or update) the function
try:
    resp = lam.create_function(
        FunctionName=FUNCTION_NAME,
        Runtime=RUNTIME,
        Role=role_arn,
        Handler=HANDLER,
        Code={"ZipFile": zip_bytes},
        Timeout=30,
        Description="hello world lambda for the exercise",
    )
    print(f"created function {FUNCTION_NAME} -> {resp['FunctionArn']}")
except lam.exceptions.ResourceConflictException:
    resp = lam.update_function_code(
        FunctionName=FUNCTION_NAME, ZipFile=zip_bytes
    )
    print(f"function {FUNCTION_NAME} already existed, updated its code")
