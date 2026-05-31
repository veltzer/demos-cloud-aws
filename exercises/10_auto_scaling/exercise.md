# Auto Scaling exercise

Auto Scaling automatically adds and removes `EC2` instances so your application
has enough capacity under load and does not waste money when idle. This exercise
builds an Auto Scaling Group (`ASG`) behind a load balancer and watches it scale
out and back in.

* Make sure you are in the same region you used for the `EC2` and load balancer
    exercises, and reuse your `VPC` and its public subnets.

* This exercise builds on the `EC2` and load balancer exercises. You should
    already understand subnets, security groups, and how an `ALB` forwards to a
    target group.

* **Prerequisite (restricted / student lab accounts):** the first `ASG` and the
    first `ALB` in an account each require a one-time service-linked role
    (`AWSServiceRoleForAutoScaling` and
    `AWSServiceRoleForElasticLoadBalancing`). If your role cannot create these
    (a common restriction in student labs), creation fails with an
    `iam:CreateServiceLinkedRole` `AccessDenied` error. Ask an admin to run these
    two commands once in the account before starting:

```bash
aws iam create-service-linked-role --aws-service-name elasticloadbalancing.amazonaws.com
aws iam create-service-linked-role --aws-service-name autoscaling.amazonaws.com
```

* Note: the launch template and plain `EC2` instances usually work even in a
    restricted lab; it is the `ALB` and `ASG` steps that hit the role
    restriction above.

* Create a `Launch Template` (the modern replacement for a launch
    configuration). It describes the instances the `ASG` will create:

    * Choose an Amazon Linux `AMI`.
    * Pick a small instance type, for example `t2.micro` or `t3.micro`.
    * Select a security group that allows inbound `HTTP` (port 80).
    * Add user data that installs a web server and writes the instance id to the
        page, so you can tell the instances apart:

```bash
#!/bin/bash
yum update -y
yum install -y httpd
systemctl enable --now httpd
echo "Hello from $(hostname -f)" > /var/www/html/index.html
```

* Create a `target group` (or reuse the one from the load balancer exercise) and
    an `Application Load Balancer` in front of it, if you do not already have one.

* Create an `Auto Scaling Group` using the launch template:

    * Attach it to your public subnets in at least two availability zones.
    * Set `min size = 1`, `desired capacity = 1`, `max size = 3`.
    * Attach it to the `ALB` target group so new instances automatically start
        receiving traffic and are health checked.

* Confirm the `ASG` launched one instance and that it shows as `healthy` in the
    target group. Hit the `ALB` `DNS` name in a browser and see the page.

* Manually set `desired capacity = 3` and watch the `ASG` launch two more
    instances. Refresh the `ALB` URL several times and confirm you see different
    instance ids (traffic is being spread across them).

* Set `desired capacity` back to `1` and watch the `ASG` terminate the extra
    instances.

## Scaling on a real metric

* Add a `Target Tracking` scaling policy to the group, for example: keep average
    `CPU utilization` at `50%`.

* Generate load on the instances so `CPU` rises (for example install `stress`
    via user data or `ssh` in and run `stress --cpu 1`, or use a load testing
    tool against the `ALB`).

* Watch `CloudWatch` alarms fire and the `ASG` scale out automatically toward
    `max size`. When the load stops, watch it scale back in toward `min size`.
    Note that scale-in is deliberately slower than scale-out.

Notes

* `desired capacity` is what the `ASG` tries to maintain right now. `min` and
    `max` are the bounds a scaling policy is allowed to move `desired` between.

* The `ASG` continuously replaces unhealthy instances. Terminate one of its
    instances by hand and watch the `ASG` launch a replacement to get back to
    `desired capacity`. This self-healing is a key reason to use an `ASG` even if
    you never scale.

* Spreading the `ASG` across multiple availability zones gives you resilience to
    an `AZ` failure, not just capacity.

* Scaling policies are driven by `CloudWatch` metrics and alarms, which ties this
    exercise to the `CloudWatch` exercise.

## Bonus

* Use a `Scheduled Action` to scale the group up every weekday morning and down
    every evening, simulating predictable business-hours traffic.

* Configure a `cooldown` / warmup and observe how it prevents the `ASG` from
    thrashing (scaling out and in repeatedly) when a metric hovers near the
    threshold.

* When you are done, delete the `Auto Scaling Group` first (this terminates its
    instances), then delete the launch template, target group, and load balancer
    so nothing lingers and keeps costing money.
