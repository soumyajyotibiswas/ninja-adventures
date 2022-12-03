# AWS Infrastrucutre Maintenance Using AWS Lambda and AWS EventBridge [EC2 instance daily ebs volume snapshots] [Part 1]

---

## Contents

* [Summary](#summary)
* [Architecture diagram and high level overview of all the solutions](#architecture-diagram-and-high-level-overview-of-all-the-solutions)
  * [Architecture diagram](#architecture-diagram)
  * [EC2 instance daily ebs volume snapshots](#ec2-instance-daily-ebs-volume-snapshots)
  * [EC2 instance daily ebs snapshot cleanup after X days](#ec2-instance-daily-ebs-snapshot-cleanup-after-x-days)
  * [EC2 instance daily unattached ebs volume cleanup after X days](#ec2-instance-daily-unattached-ebs-volume-cleanup-after-x-days)
  * [Deregister old EC2 Amazon machine images after X days](#deregister-old-ec2-amazon-machine-images-after-x-days)
* [AWS IAM permissions](#aws-iam-permissions)
  * [Permissions](#permissions)
  * [Trust relationship](#trust-relationship)
* [AWS EventBridge and Lambda](#aws-eventbridge-and-lambda)
* [EC2 instance daily ebs volume snapshots solution](#ec2-instance-daily-ebs-volume-snapshots-solution)
* [Coming up next](#coming-up-next)

---

## Summary

Welcome to [**PART-1**](#ec2-instance-daily-ebs-volume-snapshots) of a four part tutorial, on how to leverage AWS services like Lambda and EventBridge, to perform housekeeping on your AWS infrastructure on a schedule automatically. I am going to perform the following using AWS Lambda, EventBridge and python🐍.

* [**[PART-1]**](#ec2-instance-daily-ebs-volume-snapshots) Create EBS volume snapshots of all our AWS EC2 instances in all regions, and tag them.
* [**[PART-2]**](#ec2-instance-daily-ebs-snapshot-cleanup-after-x-days) Cleanup EBS volume snapshots from all our regions, whose age is greater than X days.
* [**[PART-3]**](#ec2-instance-daily-unattached-ebs-volume-cleanup-after-x-days) Cleanup EBS volumes from all our regions, which is not attached to a resource, and whose age is greater than X days.
* [**[PART-4]**](#deregister-old-ec2-amazon-machine-images-after-x-days) Deregister Amazon Machine Images from all our regions whose age is greater than X days.

I am going to do all those using AWS EventBridge, AWS Lambda and python. This is going to automate any manual effort of going to every region and finding artifacts related to these and performing maintenance on them.

---

## Architecture diagram and high level overview of all the solutions

### Architecture diagram

![EventBridge and AWS Lambda](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/tvr1c8x9908u6r8avs8a.png)

### EC2 instance daily ebs volume snapshots

I am going to list out all instances in all of our regions, and its associated volumes, and create EBS snapshots from them. Also I am going to add custom tags to these snapshots.

### EC2 instance daily ebs snapshot cleanup after X days

I am going to list all the EBS snapshots that we own in our regions, and then delete those older than X days.

### EC2 instance daily unattached ebs volume cleanup after X days

I am going to list all the EBS volumes that we own in our regions, and then delete those which are not attached to any resource and older than X days.

### Deregister old EC2 Amazon machine images after X days

I am going to list all the Amazon Machine Images that we own in our regions, and then delete those which are not attached to any resource and older than X days.

---

## AWS IAM permissions

[Create an IAM role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create.html) with the following permissions and trust policy.

### Permissions

Attach a permission policy template to your role which will allow for:

* AWS cloudwatch log stream creation and writing.
* Describe EC2 instances, volumes, snapshots and AMI's.
* EC2 snapshot creation and deletion.
* EC2 volume deletion.
* EC2 AMI deregistration.

```Json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:CreateLogGroup",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateSnapshot",
                "ec2:CreateTags",
                "ec2:DeleteSnapshot",
                "ec2:Describe*",
                "ec2:ModifySnapshotAttribute",
                "ec2:ResetSnapshotAttribute",
                "ec2:DeleteVolume",
                "ec2:DeregisterImage"
            ],
            "Resource": "*"
        }
    ]
}
```

### Trust relationship

Allow the lambda service access to your IAM role.

```Json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

---

## AWS EventBridge and Lambda

I am going to use [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html) to run our python code to do run our infrastructure maintenance.

I am going to use [AWS EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-get-started.html) to run our code via lambda on a schedule. I am going to define our schedule using a cron expression, to trigger daily at midnight, local to our timezone.
You can create an EventBridge rule by going to AWS EventBridge service ➡️ rules ➡️ create rule. The cron expression we will use will be **cron(30 18 * * ? *)**. I am based in India, and this translate to midnight IST timezone, which is **18:30:00 GMT**.

I am going to use [AWS Cloudwatch logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_GettingStarted.html) to log the data from our lambda runs.

---

## EC2 instance daily ebs volume snapshots solution

### Workflow and code

* The workflow that I will use is:
    > 🕛 Midnight ➡️ AWS EventBridge rule triggers ➡️ Runs Lambda code ➡️ Creates EC2 volume snapshots for all instances in each region ➡️ Logs to cloudwatch logs
* Install boto3

    ```Bash
    python3 -m pip install boto3
    ```

* Lambda code
  * Initializaing a boto3 [client](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/clients.html)

    ```Python
    ec2_client = boto3.client('ec2')
    ```

  * Fetching all regions

    ```Python
    def get_regions(ec2_client):
        return [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
    ```

  * Initializing a boto3 ec2 [resource](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/resources.html) per region

    ```Python
    ec2_resource = boto3.resource('ec2',region_name=region)
    ```

  * List all instances in the region using [instances.all()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.instances). You can use filters also if you want.

    ```Python
    instances = ec2_resource.instances.all()
    ```

  * List all volumes of each instance using [volumes.all()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.volumes). You can use filters also if you want.

    ```Python
    for instance in instances:
        volumes = instance.volumes.all()
    ```

  * Create snapshot of the volume using the [create_snapshot()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_snapshot) method. Will create a tag of 'Instance_Id' and assign it the value of the 'instance id' the volume is attached to and also a tag of 'Device' and assign it the value of the attribute 'Device' from the volume.

    ```Python
    desc = f'Backup for instance: {i.id} and volume: {v.id}.'
    tags = [
        {
            'Key':'Instance_Id',
            'Value':f'{instance.id}'
        },
        {
            'Key':'Device',
            'Value':f'{volume.attachments[0]["Device"]}'
        }
    ]
    for volume in volumes:
        snapshot = volume.create_snapshot(
            Description=desc,
            TagSpecifications=[
                {
                    'ResourceType':'snapshot',
                    'Tags': tags
                }
            ]
        )
    ```

* Putting it all together - Take a look at my [GITHUB](https://github.com/soumyajyotibiswas/ninja-adventures/blob/main/Code/Python/Projects/EC2_Instance_Snapshot_Scheduling_and_Cleanup_via_Lambda/0000006_lambda_create_daily_snapshots.py) page for the complete code.

![Lambda code](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/flmo8idobvtkphmny47u.png)

### Cloudwatch logs

![Cloudwatch logs from lambda](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ob8b4m12vn2ek92jcuab.png)

---

## Coming up next

[Part 2](#ec2-instance-daily-ebs-snapshot-cleanup-after-x-days) of this tutorial where I will talk about creating code for daily ebs snapshot cleanup older than X days.

---
