# DynamoDB exercise

`DynamoDB` is AWS's managed `NoSQL` database. Unlike a relational database you do
not define columns up front or run `SQL`; you store and retrieve items (think
`JSON` documents) by their key. It is fully managed and scales automatically, so
there is no server to run and, in `On-demand` mode, no capacity to plan. The
catch is that it is fast and cheap only when you look items up by their key:
queries that a relational database does easily (search by an arbitrary field,
join two tables) are awkward or expensive here, so the shape of your key matters
a lot. In this exercise you create a table, put and fetch items by key from
`python`, and see what `scan` costs you.

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
