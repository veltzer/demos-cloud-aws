# EKS exercise

`EKS` (Elastic Kubernetes Service) is AWS managed `Kubernetes`. `Kubernetes` is
the standard system for running containerized applications across a fleet of
machines: you tell it *what* you want running (for example "three copies of this
web server") and it decides *where* to run them, restarts them when they crash,
and reschedules them when a machine dies. A `Kubernetes` cluster has two parts:
the **control plane** (the brain that makes those decisions) and the **worker
nodes** (the `EC2` machines that actually run your containers). Running and
upgrading the control plane yourself is hard and easy to get wrong; with `EKS`,
AWS runs the control plane for you and you only manage the worker nodes. In this
exercise you will create a cluster, connect to it, deploy an application, scale
it, and expose it to the internet.

This is the most expensive exercise in this folder: an `EKS` cluster and its
worker nodes cost real money per hour and are not free tier. The control plane
alone has a fixed hourly charge whether or not anything is running on it, and the
load balancer you create in Part 4 costs extra on top. Create it, finish the
exercise, and tear it down the same day. Do not leave it running over a weekend.

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
    infrastructure behind the scenes (`eksctl` uses `CloudFormation`). While you
    wait, you can watch the stacks being built in the `CloudFormation` console.

* When it finishes, `eksctl` updates your `kubectl` configuration so that
    `kubectl` points at the new cluster automatically. Confirm with the command
    below. You should see your worker nodes in the `Ready` state.

```bash
kubectl get nodes
```

* You asked for `--nodes 2`, so you should see two nodes, each a `t3.small`
    `EC2` instance. Find them in the `EC2` console too: these are ordinary
    instances that `eksctl` created and joined to the cluster for you.

## Part 3: deploy an application

* Deploy a simple `nginx` web server:

```bash
kubectl create deployment web --image=nginx
```

* Confirm the pod is running:

```bash
kubectl get pods
```

* A `pod` is the smallest unit `Kubernetes` runs: one (or a few) containers
    together. The `deployment` you just created is a higher-level object that
    makes sure a given number of identical pods are always running. If a pod
    dies, the deployment starts a new one.

* Prove that self-healing to yourself. Delete the pod by name and immediately
    list pods again; you will see `Kubernetes` create a replacement so the count
    goes back to one:

```bash
kubectl delete pod [pod-name]
kubectl get pods
```

## Part 4: scale the application

* Tell the deployment you want three copies instead of one:

```bash
kubectl scale deployment web --replicas=3
```

* List the pods again and watch the count grow to three. With `-o wide` you can
    see which worker node each pod landed on; `Kubernetes` spreads them across
    your nodes:

```bash
kubectl get pods -o wide
```

* This is the core idea of `Kubernetes`: you change the *desired state*
    (one replica becomes three) and the system makes reality match it, without
    you choosing machines or starting processes yourself.

## Part 5: expose it to the internet

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

* The `service` is what gives your pods a single stable address. Pods come and
    go and each gets its own internal `IP`, but the service load-balances across
    whichever pods are currently alive, so callers never need to know the
    individual pod `IPs`. Because you asked for `type=LoadBalancer`, `EKS` went a
    step further and created a real AWS load balancer in front of the service so
    it is reachable from the internet.

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

* `kubectl get pods` shows your pods in the `default` namespace. The pods that
    run `Kubernetes` itself live in the `kube-system` namespace and are hidden
    unless you ask for them. To see everything across all namespaces use:

```bash
kubectl get pods --all-namespaces
```

* If a pod is stuck in `Pending` it usually means there is nowhere to run it:
    your nodes may be full, or there may be no nodes at all. `kubectl describe
    pod [pod-name]` shows the reason at the bottom under `Events`. `describe` is
    the first command to reach for whenever something is not as expected.

* The `EXTERNAL-IP` is a `DNS` name, not a numeric `IP`, because AWS load
    balancers are addressed by name. This is the same load balancer concept as
    the load balancer exercise, only created for you by `Kubernetes` instead of
    by hand.

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

## Bonus

* Instead of creating the deployment and service with imperative `kubectl
    create`/`expose` commands, write a `YAML` manifest that describes the same
    deployment and service, and apply it with `kubectl apply -f web.yaml`. This
    is how real `Kubernetes` work is done: the desired state lives in files you
    can commit to `git`, the same idea as the `Terraform` exercise.

* Watch the cluster react in real time. Run `kubectl get pods -w` in one
    terminal (the `-w` watches for changes) and, in another, delete a pod or
    change the replica count. You will see the events stream as `Kubernetes`
    converges back to the desired state.

* Roll out a new version: change the deployment's image to a different tag with
    `kubectl set image`, and watch `kubectl rollout status deployment/web`
    replace the pods one at a time without downtime. Then roll it back with
    `kubectl rollout undo`.
