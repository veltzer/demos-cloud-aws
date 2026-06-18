# Creating an access key in the AWS console

Many of these exercises run `python` (`boto3`) or the AWS `CLI` from your own
laptop. For that code to talk to AWS it needs an **access key**: a pair made of
an *Access Key ID* and a *Secret Access Key*. This guide shows how to create one
from the AWS web console and configure it on your machine.

A few things to know before you start:

* The secret key is shown **only once**, at the moment you create it. If you
    lose it you cannot look it up later; you have to create a new key.

* An access key is a long-lived password for your account. Treat it like one:
    never commit it to `git`, never paste it into chat or email, and delete it
    when you no longer need it.

* Prefer creating a dedicated `IAM` user (or using your existing `IAM` user)
    rather than making a key for the account root user. Root keys are strongly
    discouraged by AWS.

## Create an IAM user (skip if you already have one)

1. Sign in to the [AWS console](https://console.aws.amazon.com/).

2. Go to the `IAM` service (search for "IAM" in the top search bar).

3. In the left menu choose `Users`, then `Create user`.

4. Give the user a name (for example your own name) and click `Next`.

5. For permissions, attach the policies the exercise needs. For the course you
    can attach a broad managed policy such as `AmazonSQSFullAccess`,
    `AmazonS3FullAccess`, etc., or `AdministratorAccess` for simplicity in a
    throwaway training account. Click `Next`, then `Create user`.

## Create the access key

1. In `IAM` -> `Users`, click the user you want the key for.

2. Open the `Security credentials` tab.

3. Scroll to `Access keys` and click `Create access key`.

4. Choose a use case. Pick `Command Line Interface (CLI)` (or
    `Local code` / `Application running outside AWS`). Acknowledge the warning
    and click `Next`.

5. (Optional) add a description tag, then click `Create access key`.

6. You now see the **Access key ID** and the **Secret access key**. Click
    `Show` to reveal the secret, and either copy both values somewhere safe or
    click `Download .csv file`. This is your only chance to see the secret.

## Configure the key on your machine

The easiest way is the AWS `CLI`, which stores the key under `~/.aws/` where
`boto3` and the `CLI` find it automatically:

```bash
aws configure
```

It asks for four things:

* `AWS Access Key ID` — paste the Access Key ID.
* `AWS Secret Access Key` — paste the Secret Access Key.
* `Default region name` — use the region your resources live in, e.g.
    `us-east-1`.
* `Default output format` — `json` is fine.

This writes `~/.aws/credentials` (the keys) and `~/.aws/config` (region and
output). To check it works:

```bash
aws sts get-caller-identity
```

If it prints your account and user, the key is configured correctly.

## Rotating or deleting a key

When you are done with the exercises, or if a key may have leaked, delete it:

1. `IAM` -> `Users` -> your user -> `Security credentials` -> `Access keys`.

2. Find the key by its Access Key ID, choose `Actions` -> `Deactivate`, then
    `Delete`.

To rotate, create a new key, update `aws configure` with the new values, verify
with `aws sts get-caller-identity`, then delete the old key.

## Common problems

* `Unable to locate credentials`: you never ran `aws configure`, or you ran it
    as a different OS user (or inside `WSL`, which has its own home directory —
    run `aws configure` there too).

* `InvalidClientTokenId` / `SignatureDoesNotMatch`: the key was mistyped, has a
    trailing space, or was deleted/deactivated in the console. Re-run
    `aws configure`, or create a fresh key.

* `AccessDenied` on a specific action: the key is valid but the `IAM` user lacks
    permission for that action. Attach the right policy to the user.

* Region mismatch: the key works but your resource "does not exist". Make sure
    the default region (or the `region_name` in your code) matches where you
    created the resource.
