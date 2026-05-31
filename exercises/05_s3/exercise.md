# S3 exercise

* Create an `S3` bucket (give it a name that includes your name).

* Bucket names are globally unique across all of AWS, not just your account, so
    you may need to try a few names before one is free.

* Pay attention to the region you create the bucket in.

* Upload a file to your bucket from the console.

* Download it back to your laptop and confirm it is the same file.

* Write a `python` script using `boto3` that uploads a file, lists the objects
    in the bucket, and downloads a file.

* Run the script from your laptop.

Notes

* You need credentials on your laptop for `boto3` to work (see the `SQS`
    exercise: create an `IAM` user, install the AWS `CLI`, run `aws configure`).
    Never commit your keys to `git`.

* By default new buckets block all public access. This is a good thing. For this
    exercise keep the bucket private and access it only through your credentials.

* A minimal `python` example looks like this:

```python
import boto3

s3 = boto3.client("s3", region_name="us-east-1")
bucket = "my-bucket-yourname"

# upload
s3.upload_file("local.txt", bucket, "remote.txt")

# list
for obj in s3.list_objects_v2(Bucket=bucket).get("Contents", []):
    print(obj["Key"], obj["Size"])

# download
s3.download_file(bucket, "remote.txt", "downloaded.txt")
```

* The object `key` is the name of the object inside the bucket. It can contain
    `/` characters, which the console shows as folders, but `S3` has no real
    folders.

## Hosting a static web server out of the bucket

`S3` can serve a bucket's contents directly over `HTTP` as a static website (no
`EC2` instance, no web server process to manage). This is how you turn the
bucket into a simple web server.

* Create a second bucket for this part (give it a name that includes your name),
    or reuse your bucket if you are happy to make it public. Keep the *private*
    bucket from the main exercise private.

* Create an `index.html` and upload it as the object key `index.html`:

```html
<!doctype html>
<html><body><h1>Hello from S3</h1></body></html>
```

* Enable static website hosting on the bucket and set the index document to
    `index.html` (optionally an error document such as `error.html`):

```bash
aws s3 website s3://my-website-yourname/ --index-document index.html
```

* Unlike the main exercise, a website bucket must be reachable *without*
    credentials, so you must do two things that the private exercise told you to
    avoid:

    1. Turn off `Block Public Access` for this bucket.
    2. Attach a bucket policy that allows public `s3:GetObject`:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "PublicReadGetObject",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::my-website-yourname/*"
  }]
}
```

* Open the website endpoint in a browser. The URL form is:

```
http://<bucket-name>.s3-website-<region>.amazonaws.com
```

    (the exact host varies by region; the console shows the endpoint under
    Properties -> Static website hosting). Note this is `http`, served from the
    `s3-website-` host, which is different from the normal `s3.amazonaws.com`
    object URL.

* Confirm you can reach the page with `curl` and no credentials:

```bash
curl http://my-website-yourname.s3-website-us-east-1.amazonaws.com
```

* Think about why this is *not* the same as the presigned URL below: the website
    is permanently public to everyone, while a presigned URL grants temporary
    access to a private object.

* When you are done, remember to re-enable `Block Public Access` or delete the
    website bucket so you do not leave public data lying around.

## Bonus

* Generate a `presigned URL` for one of your objects and open it in a browser.
    This lets someone download a private object for a limited time without
    needing AWS credentials.

```python
url = s3.generate_presigned_url(
    "get_object",
    Params={"Bucket": bucket, "Key": "remote.txt"},
    ExpiresIn=3600,
)
print(url)
```

* Enable versioning on the bucket, upload the same key twice, and see both
    versions.

* When you are done, empty the bucket (you cannot delete a non-empty bucket) and
    then delete the bucket so it does not linger.
