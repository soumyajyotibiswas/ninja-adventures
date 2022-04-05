# AWS Infrastrucutre Maintenance Using AWS Lambda and AWS EventBridge [EC2 instance ebs snapshot cleanup after X days] [Part 2]

---

## Contents

* [Summary](#summary)
* [Architecture diagram and high level overview of all the solutions](#architecture-diagram-and-high-level-overview-of-all-the-solutions)
  * [Architecture diagram](#architecture-diagram)
  * [EC2 instance daily ebs volume snapshots](#ec2-instance-daily-ebs-volume-snapshots)
  * [EC2 instance daily ebs snapshot cleanup after X days](#ec2-instance-daily-ebs-snapshot-cleanup-after-x-days)
* [AWS IAM permissions](#aws-iam-permissions)
  * [Permissions](#permissions)
  * [Trust relationship](#trust-relationship)
* [AWS EventBridge and Lambda](#aws-eventbridge-and-lambda)
* [EC2 instance ebs snapshot delete solution](#ec2-instance-ebs-snapshot-delete-solution)
* [Coming up next](#coming-up-next)

---

## Summary

Welcome to [**PART-2**](#ec2-instance-daily-ebs-snapshot-cleanup-after-x-days) of a four part tutorial, on how to leverage AWS services like Lambda and EventBridge, to perform housekeeping on your AWS infrastructure on a schedule automatically. In my last [post](https://dev.to/soumyajyotibiswas/aws-infrastrucutre-maintenance-using-aws-lambda-and-aws-eventbridge-ec2-instance-daily-ebs-volume-snapshots-part-1-1b9p), I talked about how to create EBS snapshots of an instance using python, AWS lambda and AWS eventbridge. In this post we will talk about building the second part, where old EBS snapshots will be cleaned up automatically. 'Old' will be defined as a number of days, in this case 7.

* [**[PART-1]**](#ec2-instance-daily-ebs-volume-snapshots) Create EBS volume snapshots of all our AWS EC2 instances in all regions, and tag them. You can find the link to the post [here](https://dev.to/soumyajyotibiswas/aws-infrastrucutre-maintenance-using-aws-lambda-and-aws-eventbridge-ec2-instance-daily-ebs-volume-snapshots-part-1-1b9p).
* [**[PART-2]**](#ec2-instance-daily-ebs-snapshot-cleanup-after-x-days) Cleanup EBS volume snapshots from all our regions, whose age is greater than X days.

---

## Architecture diagram and high level overview of all the solutions

### Architecture diagram

![EventBridge and AWS Lambda](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/tvr1c8x9908u6r8avs8a.png)

### EC2 instance daily ebs volume snapshots

I am going to list out all instances in all of our regions, and its associated volumes, and create EBS snapshots from them. Also I am going to add custom tags to these snapshots.

### EC2 instance daily ebs snapshot cleanup after X days

I am going to list all the EBS snapshots that we own in our regions, and then delete those older than X days.

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

## EC2 instance ebs snapshot delete solution

### Workflow and code

* The workflow that I will use is:
    > 🕛 Midnight ➡️ AWS EventBridge rule triggers ➡️ Runs Lambda code ➡️ Checks EBS snapshots, and if they are created more than 7 days back, deletes them ➡️ Logs to cloudwatch logs
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

  * Initializing a boto3 ec2 [client](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#client) per region

    ```Python
    ec2_client = boto3.client('ec2',region_name=region)
    ```

  * List all snapshots in the region for the account id using [describe_snapshots(OwnerIds=[account_id])](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_snapshots).

    ```Python
    def get_snapshots_from_a_region(ec2_client,account_id):
    return (ec2_client.describe_snapshots(OwnerIds=[account_id])['Snapshots'])
    ```

  * Compare the age of the snapshots to current date and time, and if the difference is greater than 7 days, delete the snapshot. We will use the [delete_snapshot()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.delete_snapshot) method of the client to perform this activity.

    ```Python
    def get_age_of_snapshot(snap):
    return ((datetime.now() - snap['StartTime'].replace(tzinfo=None)).days)

    def delete_snapshot_from_a_region(ec2_client,snap):
    ec2_client.delete_snapshot(SnapshotId=snap['SnapshotId'])
    ```

* Putting it all together - Take a look at my [GITHUB](https://github.com/soumyajyotibiswas/ninja-adventures/blob/main/Code/Python/Projects/EC2_Instance_Snapshot_Scheduling_and_Cleanup_via_Lambda/0000007_lambda_remove_snapshots_7_days_old.py) page for the complete code.

![Lambda code](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ql5l92gm21d57avokp7k.png)

### Cloudwatch logs

![Cloudwatch logs from lambda](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/yywcnbykycdxvn4n2w5a.png)

---

## Coming up next

[Part 3](https://dev.to/soumyajyotibiswas/aws-infrastrucutre-maintenance-using-aws-lambda-and-aws-eventbridge-ec2-instance-daily-ebs-volume-snapshots-part-1-1b9p#ec2-instance-daily-unattached-ebs-volume-cleanup-after-x-days) of this tutorial where I will talk about cleaning up unattached ebs volumes after X days.

---
