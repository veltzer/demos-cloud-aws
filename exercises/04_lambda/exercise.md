# Lambda exercise

* Create a lambda function that simply prints "hello, world!"

* Use any language you like (easiest is `python` but you can use other
    languages).

* When you create the function you must choose a runtime (for example
    `python 3.x`) that matches the language and version of your code.

* Your code must define a handler function with the signature the runtime
    expects. In `python` it looks like this:

```python
def handler(event, context):
    print("hello, world!")
    return {"statusCode": 200, "body": "hello, world!"}
```

* When you create the function in the console you must also let AWS create an
    execution role for it (or supply one). This is an `IAM` role that gives the
    function permission to write its logs to `CloudWatch`. Without it the
    function cannot run.

* Make sure the handler you configure (for example `lambda_function.handler`)
    matches the file name and function name in your code. A mismatched handler
    name is the most common reason a lambda fails to start.

* Package the lambda function using AWS instructions.

* For `python` with no extra dependencies you can paste the code directly in the
    console editor. To deploy from a file, zip the source (the `.py` file must be
    at the top level of the zip, not inside a nested directory) and upload the
    `.zip`.

* Deploy your lambda function (you can use the AWS `CLI` tools or other options).

* Run your lambda function. You can do that from the console or using the `CLI`
    tools.

* In the console use the `Test` button and create a test event (any `JSON`, even
    `{}`, is fine for this exercise). Check the output and the logs in
    `CloudWatch`.

## Phase II

* Trigger your lambda function each time you get a message in your message queue.

* Use the `SQS` queue from the `SQS` exercise as the trigger (an event source
    mapping). You add this under the `Triggers` section of the function.

* For this to work the function's execution role needs permission to read from
    the queue (`ReceiveMessage`, `DeleteMessage`, `GetQueueAttributes`). The
    `AWSLambdaSQSQueueExecutionRole` managed policy grants exactly these.

* When `SQS` triggers a lambda, the messages arrive inside `event["Records"]`,
    and `SQS` deletes them automatically once your function returns successfully.
    You do not call `delete_message` yourself in this case.

* Send a message to the queue (from the console or with the `SQS` exercise
    script) and confirm in `CloudWatch` logs that your function ran.
