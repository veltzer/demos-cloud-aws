#!/usr/bin/env python
"""
Download the passwd file from the jblabs-mark-veltzer-2 bucket
"""

import boto3

BUCKET = "jblabs-mark-veltzer-2"
KEY = "passwd"
LOCAL_FILE = "passwd"

client = boto3.client("s3")
client.download_file(BUCKET, KEY, LOCAL_FILE)
print(f"downloaded s3://{BUCKET}/{KEY} -> {LOCAL_FILE}")
