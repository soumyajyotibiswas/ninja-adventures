import boto3

def get_regions(ec2_client):
    return [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

def get_instances(ec2_resource):
    return ec2_resource.instances.all()

def create_snapshot_from_volume(instance,volume):
    desc = f'Backup for instance: {instance.id} and volume: {volume.id}.'
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
    snapshot = volume.create_snapshot(
        Description=desc,
        TagSpecifications=[
            {
                'ResourceType':'snapshot',
                'Tags': tags
            }
        ]
    )
    return snapshot

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    regions = get_regions(ec2_client)
    for region in regions:
        print(f"Working on instances in region: {region}")
        ec2_resource = boto3.resource('ec2',region_name=region)
        instances = get_instances(ec2_resource)
        for instance in instances:
            print(f"Fetching volumes for instance id: {instance.id}")
            for volume in instance.volumes.all():
                try:
                    print(f"Creating snapshot for instance: {instance.id} from volume: {volume.id} in region: {region}")
                    snapshot = create_snapshot_from_volume(instance,volume)
                    print(f"Created snapshot: {snapshot.id} for instance: {instance.id} from volume: {volume.id} in region: {region}")
                except Exception as e:
                    print("Error encountered while creating snapshot. See details below.")
                    print(e)