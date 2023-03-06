import boto3
from datetime import datetime
age_of_ami = 180 # In days

def get_account_id(sts_client):
    return sts_client.get_caller_identity()['Account']

def get_regions(ec2_client):
    return [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

def get_amis(ec2_client,AccountId):
    current_time = datetime.now()
    return [image for image in ec2_client.describe_images(Owners=[AccountId])['Images'] if (current_time - datetime.strptime(image['CreationDate'], "%Y-%m-%dT%H:%M:%S.%fZ")).days > age_of_ami]

def deregister_amis(ami,ec2_client):
    print(f"Initiating deregistration of ami: {ami['ImageId']}.")
    try:
        ec2_client.deregister_image(
            ImageId=ami['ImageId'],
            DryRun=False
        )
    except Exception as e:
        print(e)

def lambda_handler(event,context):
    sts_client = boto3.client('sts')
    ec2_client = boto3.client('ec2')
    AccountId = get_account_id(sts_client)
    regions = get_regions(ec2_client)
    for region in regions:
        print(f"Fetching AMI information from region: {region}.")
        ec2_client = boto3.client('ec2',region_name=region)
        amis = get_amis(ec2_client,AccountId)
        for ami in amis:
            deregister_amis(ami,ec2_client)