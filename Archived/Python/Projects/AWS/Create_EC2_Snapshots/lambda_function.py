"""
Creates snapshots out of running / stopped ec2 instances.
"""

from typing import Dict

from lambda_helpers import get_client, get_regions


def lambda_handler(event: Dict ,context: 'awslambdaric.lambda_context.LambdaContext'):
    """
    Primay event handler

    Args:
        event (Dict): lambda event
        context (awslambdaric.lambda_context.LambdaContext): lambda context
    """
    # Get all regions
    regions = get_regions()
    # Iterate all regions
    for region in regions:
        print(f"Looking for instances in region: {region}")
        # Create EC2 client
        ec2_client = get_client(client_type='ec2',region=region)
        # Fetch instances
        instances = ec2_client.describe_instances(
            Filters=[
                {
                    'Name': 'instance-state-name',
                    'Values': [
                        'running',
                        'stopped'
                    ]
                },
            ]
        )
        # If instances are present, create snapshots
        if len(instances['Reservations']) > 0:
            instance_count=len(instances['Reservations'][0]['Instances'])
            print(f"Instances found in region: {region} is {instance_count}.")
            if instance_count > 0:
                instances_t = instances['Reservations'][0]['Instances']
                instance_ids = [instance['InstanceId'] for instance in instances_t]
                # Create snapshots
                for instance_id in instance_ids:
                    response = ec2_client.create_snapshots(
                        Description=f'Created from instance_id: {instance_id}.',
                        InstanceSpecification={
                            'InstanceId': instance_id
                        },
                        TagSpecifications=[
                            {
                                'ResourceType': 'snapshot',
                                'Tags': [
                                    {
                                        'Key': 'Instance_Id',
                                        'Value': instance_id
                                    },
                                    {
                                        'Key': 'CreatedBy',
                                        'Value': 'Lambda_Auto_Snapshot'
                                    }
                                ]
                            },
                        ],
                        DryRun=False
                    )
                    print(f"Created snapshot with id: {response['Snapshots'][0]['SnapshotId']}.")
        else:
            print(f"Instances found in region: {region} is 0.")
