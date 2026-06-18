#!/usr/bin/env python
"""
Phase II teardown: remove the SQS trigger (event source mapping)

Finds the mapping that connects the queue to the function and deletes it. The
function and the queue themselves are left alone.
"""

import boto3

FUNCTION_NAME = "mark-veltzer"
REGION = "us-east-1"

lam = boto3.client("lambda", region_name=REGION)

mappings = lam.list_event_source_mappings(
    FunctionName=FUNCTION_NAME,
)["EventSourceMappings"]

if not mappings:
    print(f"no event source mappings on {FUNCTION_NAME}")
    raise SystemExit

for mapping in mappings:
    uuid = mapping["UUID"]
    lam.delete_event_source_mapping(UUID=uuid)
    print(f"deleted event source mapping {uuid} ({mapping['EventSourceArn']})")
