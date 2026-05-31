# EKS exercise

`EKS` is AWS managed `Kubernetes`. In this exercise you will create a cluster,
connect to it, deploy an application, and expose it to the internet.

This is the most expensive exercise in this folder: an `EKS` cluster and its
worker nodes cost real money per hour and are not free tier. Create it, finish
the exercise, and tear it down the same day.

## Part 1: tools

* Install the following command line tools on your laptop:
    * the AWS `CLI` (and run `aws configure` so your credentials and region are
        set).
    * `kubectl`, the `Kubernetes` client.
    * `eksctl`, the easiest way to create an `EKS` cluster.

## Part 2: create the cluster

* Create a cluster with `eksctl`. This single command creates the `VPC`,
    subnets, the control plane and a group of worker nodes for you:

```bash
eksctl create cluster --name [yourname]-cluster --region us-east-1 --nodes 2 --node-type t3.small
```

* This takes about 15 to 20 minutes. Be patient; it is creating a lot of
    infrastructure behind the scenes (`eksctl` uses `CloudFormation`).

* When it finishes, `eksctl` updates your `kubectl` configuration so that
    `kubectl` points at the new cluster automatically. Confirm with the command
    below. You should see your worker nodes in the `Ready` state.

```bash
kubectl get nodes
```

## Part 3: deploy an application

* Deploy a simple `nginx` web server:

```bash
kubectl create deployment web --image=nginx
```

* Confirm the pod is running:

```bash
kubectl get pods
```

## Part 4: expose it to the internet

* Expose the deployment with a service of type `LoadBalancer`. On `EKS` this
    automatically provisions an AWS load balancer for you:

```bash
kubectl expose deployment web --port=80 --type=LoadBalancer
```

* Find the external address of the service (this is the load balancer DNS name):

```bash
kubectl get service web
```

* The `EXTERNAL-IP` column shows `<pending>` for a minute or two while AWS
    provisions the load balancer. Wait until a DNS name appears, then open it in
    a browser. You should see the `nginx` welcome page.

Notes

* `EKS` needs `IAM` permissions to create. If `eksctl` fails immediately with a
    permissions error, your `IAM` user does not have enough rights. For a
    learning account, admin access is the simplest fix.

* `kubectl` talks to whatever cluster your config currently points at. If
    `kubectl get nodes` fails with an authentication error, re-point it with:

```bash
aws eks update-kubeconfig --name [yourname]-cluster --region us-east-1
```

* Pay attention to the region. The cluster, the nodes and your `kubectl` config
    must all agree on one region.

## Clean up (important)

* Delete the `LoadBalancer` service first so AWS removes the load balancer it
    created:

```bash
kubectl delete service web
```

* Then delete the whole cluster with `eksctl`, which tears down the nodes, the
    control plane and the `VPC` it created:

```bash
eksctl delete cluster --name [yourname]-cluster --region us-east-1
```

* Double check in the console that the cluster, the worker `EC2` instances and
    the load balancer are all gone. A forgotten `EKS` cluster is an expensive
    mistake.
