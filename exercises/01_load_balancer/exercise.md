# AWS Load Balancer Setup Exercise

## Objective
In this exercise, you will set up an Application Load Balancer (ALB) in AWS to distribute traffic between two EC2 instances running a simple web application.

## Prerequisites
- An AWS account with appropriate permissions
- Basic knowledge of AWS EC2 and VPC concepts
- Basic understanding of networking concepts
- AWS CLI installed and configured (optional)

## Exercise Steps

### Part 1: Prepare the Infrastructure

1. First, create a VPC if you don't have one:
    - Navigate to VPC Dashboard
    - Click "Create VPC"
    - Name: `lb-exercise-vpc`
    - IPv4 CIDR: `10.0.0.0/16`
    - Create two public subnets in different availability zones:
        - Subnet 1: `10.0.1.0/24` (us-east-1a)
        - Subnet 2: `10.0.2.0/24` (us-east-1b)

1. Create an Internet Gateway:
    - Name: `lb-exercise-igw`
    - Attach it to your VPC
    - Update route tables to allow internet access

### Part 2: Launch EC2 Instances

1. Launch two EC2 instances:
    - Amazon Linux 2 AMI
    - t2.micro instance type
    - Place in different subnets
    - Add the following user data script:

```bash
#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
echo "<h1>Hello from Instance $(hostname -f)</h1>" > /var/www/html/index.html
```

1. Configure Security Group for EC2:
    - Name: `web-server-sg`
    - Inbound Rules:
        - HTTP (80) from ALB security group
        - SSH (22) from your IP

### Part 3: Create the Load Balancer

1. Navigate to EC2 Dashboard > Load Balancers
1. Click "Create Load Balancer"
1. Choose "Application Load Balancer"
1. Configure the ALB:
    - Name: `exercise-alb`
    - Scheme: internet-facing
    - IP address type: ipv4
    - Select your VPC and both subnets
    - Create new security group:
        - Name: `alb-sg`
        - Allow HTTP (80) from anywhere
1. Configure Listeners and Routing:
    - Protocol: HTTP
    - Port: 80
    - Create new target group:
        - Name: `web-servers-tg`
        - Protocol: HTTP
        - Port: 80
        - Target type: Instance
1. Add your EC2 instances to the target group

### Part 4: Testing

1. Wait for the Load Balancer to become active
1. Get the DNS name of your load balancer
1. Test accessing the application:
    - Open the DNS name in a browser
    - Refresh multiple times to see requests being distributed
    - You should see the hostname changing between refreshes

### Part 5: Clean Up

Remember to delete resources in this order to avoid additional charges:
1. Load Balancer
1. Target Group
1. EC2 Instances
1. Security Groups
1. VPC and associated resources

## Expected Outcome
- A functioning Application Load Balancer distributing traffic between two EC2 instances
- Ability to see different instance responses when refreshing the browser
- Understanding of basic AWS networking and load balancing concepts

## Bonus Challenges

1. Add health checks to your target group:
    - Path: `/health.html`
    - Create the health check file on your instances
    - Test failover by stopping the web server on one instance

1. Enable sticky sessions:
    - Configure session stickiness in your target group
    - Test using browser tools to verify session persistence

1. Add HTTPS:
    - Create an SSL certificate using AWS Certificate Manager
    - Add HTTPS listener to your ALB
    - Configure redirect from HTTP to HTTPS

## Troubleshooting Tips

1. If instances are unhealthy:
    - Verify security group rules
    - Check that web server is running
    - Verify network ACLs and route tables

1. If cannot access ALB:
    - Verify ALB security group
    - Check VPC settings and internet gateway
    - Verify listener configuration

1. For connectivity issues:
    - Use EC2 instance connect to verify web server status
    - Check instance logs: `/var/log/httpd/access_log`
    - Verify subnet routing configuration
