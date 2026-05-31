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
