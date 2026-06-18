# Lambda scripts

Helper `python` scripts for the [Lambda exercise](exercise.md). They create the
function (and its execution role), invoke it, read its logs, then wire it up to
the SQS queue from the [SQS exercise](../02_sqs) as a trigger.

## Setup

Install `boto3`:

```bash
pip install boto3
```

Configure your AWS credentials (stores access key, secret key and default
region under `~/.aws/`, where `boto3` finds them automatically):

```bash
aws configure
```

## Configure the scripts

Each script has constants at the top. Edit them to match your setup:

* `FUNCTION_NAME` / `ROLE_NAME` — change `mark-veltzer` to your own name.
* `QUEUE_NAME` — must match the queue from the SQS exercise (Phase II only).
* `REGION` — must match the region your resources live in (default `us-east-1`).

## Files

* `lambda_function.py` — the handler (`lambda_function.handler`) that prints
  "hello, world!". It also prints any SQS message bodies it is given.

## Phase I — create, run, inspect

```bash
# 1. create the execution role, zip the code, and create the function
python create_function.py

# 2. invoke it directly (the CLI version of the console Test button)
python invoke_function.py

# 3. read its CloudWatch logs to confirm "hello, world!"
python read_logs.py
```

## Phase II — trigger from SQS

First create the queue from the SQS exercise (`../02_sqs/create_queue.py`).

```bash
# 1. give the role SQS read permission and add the queue as a trigger
python add_sqs_trigger.py

# 2. send a message (use the SQS exercise script)
python ../02_sqs/put_message.py

# 3. confirm the function ran (give it a few seconds first)
python read_logs.py
```

## Teardown

```bash
# remove the SQS trigger (Phase II)
python remove_sqs_trigger.py

# delete the function, its log group, and the execution role
python delete_function.py
```

## Notes

* The handler string `lambda_function.handler` is `[file name without .py]` +
  `.` + `[function name]`. A mismatch is the most common reason a lambda fails
  to start ("handler not found").
* `create_function.py` sleeps ~10s after creating the role because a fresh IAM
  role takes a moment to become usable by lambda.
* When SQS triggers the function, messages arrive in `event["Records"]` and SQS
  deletes them automatically once the function returns successfully — you do not
  call `delete_message` yourself. If the function throws, the messages reappear
  and keep being retried; check the logs.
* Re-running `create_function.py` is safe: it reuses an existing role and updates
  the code if the function already exists.
