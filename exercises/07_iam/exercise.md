# IAM exercise

`IAM` (Identity and Access Management) is how AWS decides who can do what. This
exercise makes the rules of `IAM` concrete by creating a user with deliberately
limited permissions and seeing those limits in action.

* Create a new `IAM` user (give it a name that includes your name).

* Give the user programmatic access and download (or create) an access key for
    it.

* Do not attach any permissions yet.

* Configure the AWS `CLI` on your laptop to use this user's access key (you can
    use a named profile so you do not overwrite your main credentials):

```bash
aws configure --profile limited
```

* Try to list `S3` buckets as this user with the command below and watch it
    fail. You should get an `Access Denied` (authorization) error: the user is
    authenticated (we know who it is) but not authorized (it is allowed to do
    nothing).

```bash
aws s3 ls --profile limited
```

* Now attach a policy that grants read-only access to `S3` (the managed policy
    `AmazonS3ReadOnlyAccess`).

* Run the same command again and watch it succeed.

* Try to create a bucket as this user and watch it fail again, because the policy
    only grants read.

Notes

* Distinguish authentication (who you are, proven by your access key) from
    authorization (what you are allowed to do, decided by policies). Most AWS
    "permission" errors are authorization failures, not bad credentials.

* A policy is `JSON`. A minimal policy that allows only listing one bucket looks
    like this:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::my-bucket-yourname"
    }
  ]
}
```

* Prefer attaching policies to groups or roles rather than directly to users in
    real life. For this exercise attaching directly to the user is fine.

* `IAM` is global, not regional. There is no region selector for `IAM`.

## Bonus

* Create an `IAM` role instead of a user, with a trust policy that lets `EC2`
    assume it. Attach it to an `EC2` instance (an instance profile) and run the
    AWS `CLI` from inside the instance without configuring any access key. The
    instance gets temporary credentials automatically. This is the preferred way
    to give AWS permissions to code running on AWS, instead of long-lived keys.

* When you are done, delete the access key and the `IAM` user you created.
