import boto3
from datetime import datetime
age_of_volume = 7

def get_all_regions():
    # Get all regions and return a list
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
    return regions

def get_all_available_state_volumes(ec2_resource):
    # Get all available state volumes, and return a list
    volumes = [volume for volume in ec2_resource.volumes.filter(Filters=[{'Name':'status','Values':['available']}]) if (datetime.now() - volume.create_time.replace(tzinfo=None)).days > age_of_volume]
    return volumes

def remove_volumes(volume):
    print(f"Removing volume:{volume.id} from az {volume.availability_zone}.")
    try:
        volume.delete(DryRun=False)
    except Exception as e:
        print(e)

def lambda_handler(event,context):
    # Get all regions
    regions = get_all_regions()
    for region in regions:
        print(f"Checking for volumes in region: {region}")
        ec2_resource = boto3.resource('ec2',region_name=region)
        # Get all volumes
        volumes = get_all_available_state_volumes(ec2_resource)
        for volume in volumes:
            # Remove volume
            remove_volumes(volume)