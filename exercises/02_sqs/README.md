# SQS scripts

Helper `python` scripts for the [SQS exercise](exercise.md). They create a
queue, send a message, receive (and delete) a message, and delete the queue.

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

Each script has two constants at the top. Edit them to match your setup:

* `QUEUE_NAME` — change `mark-veltzer` to your own name.
* `REGION` — must match the region your queue lives in (default `us-east-1`).

## Running

Run the scripts in this order:

```bash
# 1. create the queue
python create_queue.py

# 2. put a message into it
python put_message.py

# 3. receive a message (and delete it after handling)
python get_message.py

# 4. delete the queue when you are done
python delete_queue.py
```

## Notes

* `get_message.py` uses long polling (`WaitTimeSeconds=10`) and may still return
  nothing on a given call — run it again if you get "no messages available".
* It deletes each message after printing it, so a message is only received once.
  A message you receive but do not delete reappears after the visibility timeout.
* After `delete_queue.py`, AWS will not let you re-create a queue with the same
  name for about 60 seconds.
