import boto3
from datetime import datetime

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    regions=[region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
    for region in regions:
        print(f"Working on instances in region:{region}")
        ec2_resource = boto3.resource('ec2',region_name=region)        
        instances = ec2_resource.instances.filter(
            Filters=[
                {'Name':'tag:Backup','Values':['True']}
            ]
        )
        # ISO 8601 timestamp
        timestamp = datetime.utcnow().replace(microsecond=0).isoformat()
        for i in instances.all():
            for v in i.volumes.all():
                desc = f'Backup for instance:{i.id} and volume {v.id}, at {timestamp}'
                tags = [
                    {
                        'Key':'Instance_Id',
                        'Value':f'{i.id}'
                    },
                    {
                        'Key':'Device',
                        'Value':f'{v.attachments[0]["Device"]}'
                    }
                ]
                print(desc)
                snapshot = v.create_snapshot(
                    Description=desc,
                    TagSpecifications=[
                        {
                            'ResourceType':'snapshot',
                            'Tags': tags
                        }
                    ]
                )
                print(f"Created snapshot: {snapshot.id} for instance: {i.id} from volume: {v.id} in region: {region}")