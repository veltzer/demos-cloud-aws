# DynamoDB exercise

* Create a `DynamoDB` table (give it a name that includes your name).

* Choose a `partition key` (also called the hash key), for example `id` of type
    `String`. This is the primary key of the table.

* Choose `On-demand` capacity mode so you do not have to think about read/write
    capacity units and so it stays in the free tier for light use.

* Pay attention to the region. The table lives in one region and your code must
    talk to that same region.

* From the console, add a couple of items to the table by hand.

* Write a `python` script using `boto3` that puts an item, gets it back by key,
    and scans the whole table.

* Run the script from your laptop.

Notes

* You need credentials on your laptop for `boto3` to work (see the `SQS`
    exercise: create an `IAM` user, install the AWS `CLI`, run `aws configure`).
    Your `IAM` user must allow the `DynamoDB` actions you use (`PutItem`,
    `GetItem`, `Scan`).

* `DynamoDB` is schema-less except for the key(s): every item must have the
    partition key, but other attributes can differ from item to item.

* A minimal `python` example looks like this:

```python
import boto3

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("my-table-yourname")

# put an item
table.put_item(Item={"id": "1", "name": "Alice", "age": 30})

# get it back by key
resp = table.get_item(Key={"id": "1"})
print(resp.get("Item"))

# scan the whole table (reads every item, avoid on large tables)
for item in table.scan().get("Items", []):
    print(item)
```

* `get_item` requires the full primary key. To fetch items without knowing the
    key you must `scan` (reads everything) or `query` (needs the partition key).
    Prefer `query` over `scan` on real tables; `scan` is fine for this exercise.

* Numbers come back as `Decimal` objects when you use the resource interface.
    This surprises many students.

## Bonus

* Add a `sort key` (range key) to a new table, for example partition key
    `user_id` and sort key `timestamp`, and store several items per user. Then
    `query` all items for one user.

* When you are done, delete the table so it does not linger.
