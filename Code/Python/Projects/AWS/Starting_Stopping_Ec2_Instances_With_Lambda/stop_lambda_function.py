"""
Stops running ec2 instances
"""

from lambda_helpers import get_regions, get_resource


def lambda_handler(event,context) -> None:
    """
    Primary lambda handler function

    Args:
        event (_type_): _description_
        context (_type_): _description_
    """
    # Get list of regions
    regions = get_regions()
    # Iterate over each region
    for region_name in regions:
        print(f"Checking for running instances in region: {region_name}")
        # Create ec2 resource
        ec2_resource = get_resource('ec2',region=region_name)
        # Get running instances
        running_instances = ec2_resource.instances.filter(
            Filters=[
                {'Name':'instance-state-name',
                'Values': ['running']}
            ]
        )
        count_of_instances=len(list(running_instances))
        print(f"Running instances in region: {region_name} is {count_of_instances}")
        # Stop running instances
        for instance in running_instances:
            instance.stop()
            print(f'Stopped instance: {instance.id}')
