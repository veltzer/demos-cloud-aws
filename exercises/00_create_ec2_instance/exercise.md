# Create your first AWS instance

Use the AWS console to create your first AWS instance.

* Make sure you are in the right region (top right corner of the console).
    Pick one region (for example `us-east-1`) and stay in it for the whole
    exercise. Resources you create in one region are invisible from another
    region, and this confuses many students.

* Create your own `VPC` named `vpc-[yourname]`

* When creating the `VPC` give it a `CIDR` block, for example `10.0.0.0/16`.

* Create at least one subnet in your `VPC`.

* Make sure your subnet is a public subnet (see notes below on how to make a
    subnet public).

* Go to the EC2 service

* Click `Launch an instance`

* Fill out the details:
    * Choose `ubuntu` as your operating system (the `AMI`).
    * Choose the `t2.micro` or `t3.micro` instance type (these are in the free
        tier so you will not be charged).
    * Choose the subnet you created as the subnet to put the instance in.
    * Enable `Auto-assign public IP` so that you get a public `IP` you can
        connect to from your laptop.
    * Create a new key pair (choose the `.pem`/`RSA` format), download it and
        keep it safe. You will need it to `ssh` into the machine. You can only
        download the private key once.
    * Create or choose a security group and open the `ssh` port (port `22`) to
        the world (`0.0.0.0/0`) so you can connect.

* When your instance comes up log in to it from your computer using `ssh`

Notes

* To connect to your instance use

```bash
ssh -i [secret_key.pem] ubuntu@[your_ip]
```

* The user name to use in `ssh` depends on the `AMI`. For `ubuntu` it is
    `ubuntu`. For Amazon Linux it is `ec2-user`. Using the wrong user name is a
    very common mistake.

* Use the public `IP` (or public `DNS` name) of the instance, not the private
    one. You can see both in the instance details in the console.

* Make sure you allow `ssh` traffic into your instance from any address
    (`0.0.0.0/0`). This is done in the security group attached to the instance.

* Make sure you launch your instance in a public subnet. A subnet is public
    when:
    * There is an internet gateway (`IGW`) attached to your `VPC`.
    * The route table associated with the subnet has a route that sends
        `0.0.0.0/0` traffic to that internet gateway.

* You may need to tighten up security on your downloaded `.pem` file using the
    command below. `ssh` will refuse to use a key file that is readable by other
    users.

```bash
chmod 400 [secret_key.pem]
```

* If your `ssh` connection just hangs (times out) it is almost always a
    networking problem: missing public `IP`, security group not allowing port
    `22`, or the subnet not being public. If you get `Permission denied` it is
    almost always the wrong user name or the wrong key file.

* When you are done, `stop` or `terminate` the instance so you do not get
    charged. `terminate` deletes the instance completely.
