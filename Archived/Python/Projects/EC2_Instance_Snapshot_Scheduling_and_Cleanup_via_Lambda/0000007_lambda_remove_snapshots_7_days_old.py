import boto3
from datetime import datetime
delete_snaps_older_than = 7 # This is in days

def get_regions(ec2_client):
    return [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

def get_account_id(sts_client):
    return sts_client.get_caller_identity()['Account']

def get_snapshots_from_a_region(ec2_client,account_id):
    return (ec2_client.describe_snapshots(OwnerIds=[account_id])['Snapshots'])

def get_age_of_snapshot(snap):
    return ((datetime.now() - snap['StartTime'].replace(tzinfo=None)).days)

def delete_snapshot_from_a_region(ec2_client,snap):
    ec2_client.delete_snapshot(SnapshotId=snap['SnapshotId'])

def lambda_handler(event, context):
    sts_client = boto3.client('sts')
    account_id= get_account_id(sts_client)
    ec2_client = boto3.client('ec2')
    regions= get_regions(ec2_client)
    for region in regions:
        print(f"Working on snapshots in region:{region}")
        ec2_client = boto3.client('ec2',region_name=region)
        snapshots = get_snapshots_from_a_region(ec2_client,account_id)
        for snap in snapshots:
            age_of_snap = get_age_of_snapshot(snap)
            if age_of_snap > delete_snaps_older_than:
                print(f"Found snapshot: {snap['SnapshotId']} in region {region} with start time {snap['StartTime']}, which is {age_of_snap} days old.")
                try:
                    print(f"Deleting snapshot: {snap['SnapshotId']} in region {region}.")
                    delete_snapshot_from_a_region(ec2_client,snap)
                except Exception as e:
                    if 'InvalidSnapshot.InUse' in e.response['Error']['Code']:
                        print(f"Snapshot: {snap['SnapshotId']} in region {region} is in use, cannot be deleted.")
                        continue   
