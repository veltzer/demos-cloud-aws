# Using PuTTY on Windows

`PuTTY` is a popular free `ssh` client for Windows. If you are on Windows and do
not want to use `WSL` or `git bash`, `PuTTY` lets you connect to the `EC2`
instances you create in the exercises.

## Install

* Download `PuTTY` from the official site (search for "PuTTY download"). Install
    the full package (the installer, not just `putty.exe`), because you also need
    `PuTTYgen`.

* The package gives you two programs you care about:
    * `PuTTY` itself, the `ssh` client.
    * `PuTTYgen`, used to convert key files.

## Convert your .pem key to .ppk

AWS gives you a private key in `.pem` format. `PuTTY` does not read `.pem`; it
needs its own `.ppk` format. You only have to do this once per key.

* Open `PuTTYgen`.

* Click `Load`.

* In the file dialog change the filter to `All Files (*.*)` (otherwise you will
    not see your `.pem` file).

* Select your `.pem` file and click `Open`.

* Click `Save private key`. `PuTTYgen` may warn that the key has no passphrase;
    that is fine for this exercise, click `Yes`.

* Save the new `.ppk` file somewhere you will remember.

## Connect to your instance

* Open `PuTTY`.

* In `Host Name (or IP address)` type your login in the form
    `ubuntu@[your_public_ip]`.

    * The user name depends on the operating system of the instance. For
        `ubuntu` instances it is `ubuntu`. For Amazon Linux it is `ec2-user`.
        Using the wrong user name is a very common mistake.

    * Use the public `IP` of the instance, not the private one.

* Make sure the `Port` is `22` and the connection type is `SSH`.

* In the left tree expand `Connection`, then `SSH`, then `Auth`, then
    `Credentials` (the exact path varies a little between `PuTTY` versions).

* Next to `Private key file for authentication` click `Browse` and select your
    `.ppk` file.

* (Optional) Go back to the `Session` screen, type a name under
    `Saved Sessions` and click `Save` so you do not have to fill everything in
    again next time.

* Click `Open`.

* The first time you connect `PuTTY` asks you to trust the host key. Click
    `Accept`.

## Common problems

* `Connection timed out`: this is a networking problem, not a `PuTTY` problem.
    Check that the instance has a public `IP`, that the security group allows
    `ssh` (port `22`) from your address, and that the subnet is public.

* `Server refused our key` or `No supported authentication methods`: you either
    pointed `PuTTY` at the `.pem` instead of the `.ppk`, or you are using the
    wrong user name.

* `Pageant` is an optional `PuTTY` agent that holds your key in memory so you do
    not select it every time. You do not need it for the exercises, but it is
    handy if you connect often.
