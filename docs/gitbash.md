# Using Git Bash on Windows

`Git Bash` is a small `Linux`-like shell that comes with `Git for Windows`. It
gives you `bash` and the common `Unix` commands (`ssh`, `chmod`, `ls`, `cat`,
`scp`, ...) without installing a full `Linux` like `WSL`. It is a good
middle-ground for the `ssh` parts of the exercises.

## Install

* Download `Git for Windows` from the official site (search for
    "Git for Windows download").

* Run the installer. The defaults are fine. When it finishes you will have a
    `Git Bash` entry in the Start menu.

* You can also install it from a terminal if you have a package manager
    (`chocolatey` users can run `choco install git` instead):

```powershell
winget install Git.Git
```

* Open `Git Bash` from the Start menu to get a `bash` shell.

## What works

* `ssh`, `scp` and `chmod` all work, so the `EC2` and `ssh` instructions in the
    exercises work as written:

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@your_public_ip
```

* The user name depends on the instance operating system: `ubuntu` for
    `ubuntu`, `ec2-user` for Amazon Linux. Use the public `IP`.

* `python` and `pip` work if you installed `python` for Windows; use them for
    the `boto3` exercises. Install `boto3` with `pip install boto3`.

## Paths in Git Bash

* `Git Bash` uses `Linux`-style paths. Your `C:` drive is `/c`, so a key in your
    Downloads folder is at `/c/Users/yourname/Downloads/your-key.pem`.

* You can drag a file from Explorer into the `Git Bash` window to paste its
    path.

## Set up the AWS CLI

* The AWS `CLI` is a separate install (it is not part of `Git for Windows`).
    Install the AWS `CLI` for Windows, then configure it from inside `Git Bash`:

```bash
aws configure
```

## Common problems

* `aws: command not found`: the AWS `CLI` is not installed, or you opened
    `Git Bash` before installing it (close and reopen `Git Bash` after
    installing so it picks up the new `PATH`).

* `Permissions ... are too open`: run `chmod 400 your-key.pem` in `Git Bash`,
    the same as on `Linux`.

* `Connection timed out`: a networking problem, not a shell problem. Check the
    public `IP`, the security group rule for port `22`, and that the subnet is
    public.
