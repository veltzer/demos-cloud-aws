# Using WSL to do the exercises on Windows

`WSL` (Windows Subsystem for Linux) runs a real `Linux` distribution inside
Windows. This is the most comfortable way to do these exercises on a Windows
machine, because every command in the exercises is written for `Linux`/`macOS`
and will work unchanged: `ssh`, `chmod`, the AWS `CLI`, `python`, `boto3`,
`Terraform`, `kubectl` and `eksctl` all behave exactly as on `Linux`.

## Install WSL

* Open `PowerShell` as Administrator and run:

```powershell
wsl --install
```

* This installs `WSL` and, by default, an `ubuntu` distribution. Reboot if it
    asks you to.

* After the reboot `ubuntu` starts automatically and asks you to create a
    `Linux` user name and password. This user is separate from your Windows
    account.

* From then on, open the `ubuntu` (or "WSL") app from the Start menu to get a
    `Linux` shell.

## Set up your tools inside WSL

Everything you install here lives inside the `Linux` environment, not Windows.

* Update the package list and install basics:

```bash
sudo apt update
sudo apt install -y python3-pip unzip
```

* Install the AWS `CLI` (follow the official `Linux` instructions), then
    configure your credentials:

```bash
aws configure
```

* Install `boto3` for the `python` exercises:

```bash
pip install boto3
```

## Working with files

* Your Windows drives are mounted under `/mnt`, so your `C:` drive is
    `/mnt/c`. You can reach a downloaded key with a path like
    `/mnt/c/Users/yourname/Downloads/your-key.pem`.

* Permissions on files under `/mnt/c` do not always behave like real `Linux`
    permissions, which breaks `chmod 400` on your `.pem` key. The simplest fix
    is to copy the key into your `WSL` home directory first:

```bash
cp /mnt/c/Users/yourname/Downloads/your-key.pem ~/
chmod 400 ~/your-key.pem
ssh -i ~/your-key.pem ubuntu@your_public_ip
```

## Common problems

* `wsl --install` not recognized: your Windows is too old. Update Windows, or
    enable `WSL` through `Turn Windows features on or off`.

* `chmod` "does not stick" on a key under `/mnt/c`: copy the key into your `WSL`
    home directory (`~`) as shown above and `chmod` it there.

* The `Linux` user inside `WSL` is not your Windows user and does not have your
    Windows AWS credentials. Run `aws configure` inside `WSL` once.
