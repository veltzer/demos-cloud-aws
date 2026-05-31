# SQS exercise

* Create an `SQS` queue (give it your name).

* Choose a `Standard` queue (not a `FIFO` queue) unless you specifically want
    to experiment with `FIFO` ordering.

* Open the `SQS` for the entire world (it is a security issue but that doesn't
    matter). This is done through the access policy of the queue.

* Write a `python` script to put/pull a message from your queue.

* Run that `python` on your laptop and see that you can insert/remove messages
    from the queue.

* You will need to configure authentication properly.

* You will need to use the `boto3` `python` library.

Notes

* Pay attention to the region. The queue lives in one region and your code must
    talk to that same region. Mismatched regions are a very common mistake.

* You need credentials on your laptop for `boto3` to work. The easiest way is to
    create an `IAM` user with programmatic access (or an access key), then
    install the AWS `CLI` and run the command below. This stores your access key,
    secret key and default region under `~/.aws/credentials` and `~/.aws/config`,
    where `boto3` will find them automatically. Never commit these keys to `git`.

```bash
aws configure
```

* Your `IAM` user (or the queue policy) must allow the `SQS` actions you use
    (`SendMessage`, `ReceiveMessage`, `DeleteMessage`).

* Install `boto3` with:

```bash
pip install boto3
```

* You will need the queue `URL` (not just the name) to send and receive. You can
    get it from the console or with `get_queue_url`.

* A minimal `python` example looks like this:

```python
import boto3

sqs = boto3.client("sqs", region_name="us-east-1")
queue_url = sqs.get_queue_url(QueueName="my-queue")["QueueUrl"]

# put a message
sqs.send_message(QueueUrl=queue_url, MessageBody="hello, world!")

# pull a message
resp = sqs.receive_message(QueueUrl=queue_url, WaitTimeSeconds=10)
for msg in resp.get("Messages", []):
    print(msg["Body"])
    # you must delete the message after handling it, otherwise it
    # becomes visible again after the visibility timeout
    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=msg["ReceiptHandle"])
```

* `receive_message` does not always return a message immediately. Use
    `WaitTimeSeconds` (long polling) and try a few times if you get nothing.

* A message that you receive but do not delete will reappear after the
    `visibility timeout`. This is by design.

* When you are done, delete the queue so it does not linger.
