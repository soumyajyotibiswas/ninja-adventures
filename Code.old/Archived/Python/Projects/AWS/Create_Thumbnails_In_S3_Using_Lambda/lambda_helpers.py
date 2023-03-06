"""
Lambda helpers file
"""

import boto3


def get_client(client_type: str,region: str=None) -> 'boto3':
    """
    Returns a boto3 client of a specified type and region.

    Args:
        client_type (str): type of boto3 client needed.
        region (str, optional): region if needed. Defaults to None.

    Returns:
        boto3.client: returns boto3.client
    """
    return boto3.client(client_type,region_name=region)

def get_resource(resource_type: str,region: str=None) -> 'boto3':
    """
    Returns a boto3 resource of a specified type and region.

    Args:
        resource_type (str): type of boto3 resource needed.
        region (str, optional): region if needed. Defaults to None.

    Returns:
        boto3.resource: returns boto3.resource
    """
    return boto3.resource(resource_type,region_name=region)

def get_regions() -> list:

    """
    Return a list of AWS regions

    Returns:
        list: AWS region list
    """
    return [region['RegionName'] for region in get_client('ec2').describe_regions()['Regions']]
