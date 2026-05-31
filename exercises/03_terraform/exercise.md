# Terraform with AWS

## Stage one

* install `Terraform` on your platform

* Make sure your AWS credentials are available to `Terraform`. The simplest way
    is to install the AWS `CLI` and run `aws configure` (this writes your access
    key, secret key and region to `~/.aws`). `Terraform` reads these
    automatically.

* write a simple `Terraform` file that creates a key on `AWS`.

* Your `Terraform` file must declare the AWS provider and the region, for
    example:

```hcl
provider "aws" {
  region = "us-east-1"
}
```

* To create a key pair you supply your own public key. Generate one on your
    laptop with `ssh-keygen` if you do not already have one, then point the
    `aws_key_pair` resource at the `.pub` file.

* run and create that key using
    * `terraform init`
    * `terraform apply`

* `terraform init` downloads the AWS provider and must be run once in the
    directory before `apply`. Run `terraform plan` first if you want to see what
    will be created before it happens.

## Stage two

* now launch a machine (including `VPC`, subnet, key, security group, ...) using
    `Terraform`.

* For the machine to be reachable by `ssh` you need the same things as in the
    console exercise, only expressed in `Terraform`:
    * an `ubuntu` `AMI` (look up the `AMI` `ID` for your region, or use a data
        source to find it, since `AMI` `IDs` differ between regions).
    * a `t2.micro` or `t3.micro` instance type (free tier).
    * a `VPC` with a `CIDR` block (for example `10.0.0.0/16`).
    * an internet gateway attached to the `VPC` and a route table that sends
        `0.0.0.0/0` to it (this is what makes the subnet public).
    * a subnet inside the `VPC` with `map_public_ip_on_launch` enabled (or
        assign a public `IP` to the instance) so the machine gets a public `IP`.
    * a security group that allows inbound `ssh` (port `22`) from `0.0.0.0/0`.
    * the key pair from stage one, referenced by the instance.

* After `apply`, output the public `IP` of the instance (use an `output` block)
    so you know where to `ssh`.

Notes

* `Terraform` keeps a `terraform.tfstate` file describing what it created. Do
    not delete it by hand and do not commit it to `git` (it can contain secrets).

* `AMI` `IDs` are region specific. An `AMI` `ID` that works in one region will
    fail in another.

* When you are done, run `terraform destroy` to tear down everything you created
    so you do not get charged. This is the big advantage of `Terraform`: it
    cleans up exactly what it made.
