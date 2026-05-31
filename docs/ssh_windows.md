# Using ssh on Windows

Modern Windows ships with `OpenSSH`, the same `ssh` client used on `Linux` and
`macOS`. This means you can do the `ssh` parts of the exercises from a normal
Windows terminal without installing `PuTTY`. The catch on Windows is fixing the
permissions on the `.pem` key file, which is explained below.

## Check that ssh is available

* Open `PowerShell` (or the new Windows Terminal) and run:

```powershell
ssh -V
```

* If you see a version string, you are ready. If the command is not found,
    install the `OpenSSH` client: `Settings` then `Apps` then
    `Optional features`, add `OpenSSH Client`.

## Connect to your instance

* The command is the same as on `Linux` or `macOS`:

```powershell
ssh -i C:\path\to\your-key.pem ubuntu@your_public_ip
```

* The user name depends on the operating system of the instance: `ubuntu` for
    `ubuntu`, `ec2-user` for Amazon Linux. Use the public `IP`, not the private
    one.

## Fixing permissions on the .pem file (the Windows gotcha)

On `Linux`/`macOS` you run `chmod 400 key.pem`. On Windows there is no `chmod`,
and `ssh` will refuse to use a key that other users can read, failing with a
message like:

```text
Permissions for 'your-key.pem' are too open.
This private key will be ignored.
```

The fix on Windows is to strip inherited permissions and grant access only to
your own user. Run these in `PowerShell` from the folder that holds the key
(replace `your-key.pem` with your file name):

```powershell
# stop the file from inheriting permissions from its folder
icacls your-key.pem /inheritance:r

# grant only the current user read access
icacls your-key.pem /grant:r "$($env:USERNAME):(R)"

# remove access for everyone else who might still have it
icacls your-key.pem /remove "BUILTIN\Users" "Authenticated Users" "Everyone"
```

After this, `ssh -i your-key.pem ...` will work.

## Common problems

* `Permissions ... are too open`: you have not fixed the key file permissions;
    run the `icacls` commands above.

* `Connection timed out`: a networking problem, not an `ssh` problem. Check the
    public `IP`, the security group rule for port `22`, and that the subnet is
    public.

* `Permission denied (publickey)`: almost always the wrong user name or the
    wrong key file.

* Make sure you use the correct path to the `.pem` file. In `PowerShell` you can
    use either `\` or `/` as a path separator.
