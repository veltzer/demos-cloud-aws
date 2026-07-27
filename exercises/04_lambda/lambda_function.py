"""
The lambda handler

When invoked directly the event is whatever JSON you pass (e.g. {}).
When invoked by SQS the messages arrive in event["Records"]; SQS deletes them
automatically once this function returns successfully.

The configured handler is "lambda_function.handler" -> [this file].[this func].
"""


# "context" is part of the AWS-mandated handler signature and is unused here.
def handler(event, context):  # pylint: disable=unused-argument
    print("hello, world!")
    # if this came from SQS, print the message bodies too
    for record in event.get("Records", []):
        print(f"sqs message: {record.get('body')}")
    return {"statusCode": 200, "body": "hello, world!"}
