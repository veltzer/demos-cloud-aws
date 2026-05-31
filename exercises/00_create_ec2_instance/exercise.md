# Create your first AWS instance

Use the AWS console to create your first AWS instance.

* Create your own `VPC` named `vpc-[yourname]`

* Create at least one subnet in your `VPC`.

* Go to the EC2 service

* Click `Launch an instance`

* Choose the subnet you create as the subnet to put the instance in.

* Fill out the details, choose ubuntu as your operating system

* When your instance comes up log in to it from your compute using `ssh`

Notes
* To connect to your instance use

```bash
ssh -i [secret_key.pem] ubuntu@[your_ip]
```

* Make sure you allow ssh traffic into your instance from any address (`0.0.0.0`).

* Make sure you launch your instance in a public subnet.

* You may need to tight up security on your downloaded .pem file using

```bash
chmod 400 [secret_key.pem]
```
