# Lambda exercise

`Lambda` is AWS's serverless compute service. Instead of launching an `EC2`
instance and keeping it running, you upload a single function and AWS runs it on
demand, in response to an event, and bills you only for the milliseconds it
actually runs. There is no server for you to start, patch, or stop. The function
is short-lived: it receives an `event`, does its work, returns, and goes away. In
this exercise you write a trivial function, run it by hand, and then wire it up
so that it runs automatically whenever a message lands in the `SQS` queue from
the previous exercise.

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

Notes

* If the `Test` button reports an error like "handler not found", the handler
    string you configured does not match your code. The handler is
    `[file name without .py].[function name]` — for the example above, with a
    file `lambda_function.py`, the handler is `lambda_function.handler`.

* When `SQS` triggers the function but the messages never disappear from the
    queue and keep being retried, your function is throwing an exception. `SQS`
    only deletes the messages when the function returns successfully; a failure
    sends them back to the queue. Read the `CloudWatch` logs to find the error.

* When you are done, delete the event source mapping (the `SQS` trigger) and the
    lambda function so they do not linger. Deleting the function does not delete
    its `CloudWatch` log group; delete that too if you want a clean account.
