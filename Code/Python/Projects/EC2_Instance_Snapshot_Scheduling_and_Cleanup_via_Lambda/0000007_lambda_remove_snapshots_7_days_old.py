import boto3
from datetime import datetime
delete_snaps_older_than = 7
def lambda_handler(event, context):
    account_id=boto3.client('sts').get_caller_identity().get('Account')
    ec2_client = boto3.client('ec2')
    regions=[region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
    for region in regions:
        print(f"Working on snapshots in region:{region}")
        ec2_client = boto3.client('ec2',region_name=region)
        snapshots = ec2_client.describe_snapshots(OwnerIds=[account_id])['Snapshots']
        for snap in snapshots:
            age_of_snap = (datetime.now() - snap['StartTime'].replace(tzinfo=None)).days
            if age_of_snap > delete_snaps_older_than:
                print(f"Found snapshot: {snap['SnapshotId']} in region {region} with start time {snap['StartTime']}, which is {age_of_snap} days old.")
                try:
                    print(f"Deleting snapshot: {snap['SnapshotId']} in region {region}.")
                    ec2_client.delete_snapshot(SnapshotId=snap['SnapshotId'])
                except Exception as e:
                    if 'InvalidSnapshot.InUse' in e.response['Error']['Code']:
                        print(f"Snapshot: {snap['SnapshotId']} in region {region} is in use, cannot be deleted.")
                        continue   
