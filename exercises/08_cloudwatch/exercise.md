# CloudWatch exercise

`CloudWatch` is where AWS collects metrics, logs and alarms. This exercise has
you read metrics, read logs, and react to them with an alarm.

## Part 1: metrics

* Make sure you have a running `EC2` instance (reuse the one from the `EC2`
    exercise, or launch a small `t2.micro`).

* Go to the `CloudWatch` service and find the `CPUUtilization` metric for your
    instance.

* Generate some load on the instance so the metric moves. From inside the
    instance run the command below. It pins one CPU; kill it later with
    `kill %1`.

```bash
yes > /dev/null &
```

* Watch the `CPUUtilization` graph rise in `CloudWatch`. Metrics are not
    instant; basic `EC2` metrics arrive every 5 minutes, so be patient.

## Part 2: logs

* Find the log group for the `lambda` function you created in the `lambda`
    exercise (log groups are named `/aws/lambda/[function-name]`).

* Invoke the lambda a few times and read its log streams to see the output and
    any errors.

* If you do not have a lambda, any service that writes logs (such as the load
    balancer access logs) will do.

## Part 3: alarm

* Create a `CloudWatch` alarm on the `CPUUtilization` metric of your instance.

* Set the threshold to fire when `CPUUtilization` is above some value (for
    example 50%) for one period.

* Create an `SNS` topic and subscribe your email to it, then have the alarm
    notify that topic. Confirm the subscription from the email AWS sends you.

* Generate load again (see Part 1) and confirm that the alarm goes into the
    `ALARM` state and that you receive the notification email.

Notes

* An alarm has three states: `OK`, `ALARM` and `INSUFFICIENT_DATA`. A brand new
    alarm often sits in `INSUFFICIENT_DATA` until enough metric data arrives.
    This is normal, not a bug.

* You must confirm the `SNS` email subscription (click the link in the email)
    before you will receive any alarm notifications.

* Pay attention to the period and the number of evaluation periods. An alarm
    that needs the metric to be high for several long periods will feel like it
    "does not work" when it is simply still waiting.

* When you are done, stop the load (`kill %1`), delete the alarm and the `SNS`
    topic, and stop or terminate the instance so you do not get charged.
