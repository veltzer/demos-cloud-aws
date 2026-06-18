#
# Terraform equivalent of create_function.py + add_sqs_trigger.py
#
# This creates the same resources the boto3 scripts do:
#   - an IAM execution role the function assumes
#   - the CloudWatch-logs and SQS-read managed policy attachments
#   - the lambda function (code zipped from lambda_function.py)
#   - an SQS queue and an event source mapping wiring it to the function
#
# Usage:
#   terraform init
#   terraform apply
#   terraform destroy
#
# Names/region/runtime are kept identical to the Python scripts, so do not run
# both against the same account at once or they will collide on those names.
#

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.0"
    }
  }
}

locals {
  function_name = "mark-veltzer"
  role_name     = "mark-veltzer-lambda-role"
  queue_name    = "mark-veltzer"
  region        = "us-east-1"
  runtime       = "python3.12"
  handler       = "lambda_function.handler"
  source_file   = "lambda_function.py"
}

provider "aws" {
  region = local.region
}

# --- IAM execution role (mirrors steps 1-2 of create_function.py) -----------

# trust policy: allow the lambda service to assume this role
resource "aws_iam_role" "lambda_exec" {
  name        = local.role_name
  description = "execution role for the lambda exercise"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

# let the function write logs to CloudWatch
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# let the execution role read/delete from SQS (mirrors add_sqs_trigger.py)
resource "aws_iam_role_policy_attachment" "lambda_sqs" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole"
}

# --- the function (mirrors steps 3-4 of create_function.py) -----------------

# zip lambda_function.py with the .py at the top level of the archive
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/${local.source_file}"
  output_path = "${path.module}/lambda_function.zip"
}

resource "aws_lambda_function" "this" {
  function_name = local.function_name
  description   = "hello world lambda for the exercise"
  role          = aws_iam_role.lambda_exec.arn

  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  handler = local.handler
  runtime = local.runtime
  timeout = 30

  # ensure the role's policies are attached before the function is created,
  # the boto3 script does this with a time.sleep; terraform uses the dependency
  depends_on = [
    aws_iam_role_policy_attachment.lambda_logs,
    aws_iam_role_policy_attachment.lambda_sqs,
  ]
}

# --- SQS queue + trigger (mirrors add_sqs_trigger.py) -----------------------

resource "aws_sqs_queue" "this" {
  name = local.queue_name
}

resource "aws_lambda_event_source_mapping" "sqs_trigger" {
  event_source_arn = aws_sqs_queue.this.arn
  function_name    = aws_lambda_function.this.arn
  batch_size       = 10
  enabled          = true
}

# --- outputs ----------------------------------------------------------------

output "function_arn" {
  value = aws_lambda_function.this.arn
}

output "queue_url" {
  value = aws_sqs_queue.this.url
}

output "event_source_mapping_uuid" {
  value = aws_lambda_event_source_mapping.sqs_trigger.uuid
}
