"""
Create thumbnails in S3 using AWS Lambda
"""

import os
import tempfile
from typing import Dict

import config
from lambda_helpers import get_client
from PIL import Image


def generate_thumbnail(source_path: str, destination_path: str) -> None:
    """
    Generate a thumbnail

    Args:
        source_path (str): source path of file.
        destination_path (str): destination path of file.
    """
    with Image.open(source_path) as image:
        image.thumbnail(config.SIZE)
        image.save(destination_path)

def lambda_handler(event: Dict,context: 'awslambdaric.lambda_context.LambdaContext') -> None:
    """
    Primary lambda handler

    Args:
        event (Dict): S3 event
        context (awslambdaric.lambda_context.LambdaContext): event context.
    """
    for record in event['Records']:
        source_bucket=record['s3']['bucket']['name']
        source_region=record['awsRegion']
        s3_client = get_client(client_type='s3',region=source_region)
        source_key=record['s3']['object']['key']
        thumbnail = 'thumbnail-' + source_key
        with tempfile.TemporaryDirectory() as tmpdir:
            download_path = os.path.join(tmpdir,source_key)
            upload_path = os.path.join(tmpdir,thumbnail)
            s3_client.download_file(source_bucket, source_key, download_path)
            generate_thumbnail(source_path=download_path, destination_path=upload_path)
            s3_client.upload_file(upload_path, config.DESTINATION_BUCKET, thumbnail)
            print(f"Thumbnail image saved at {config.DESTINATION_BUCKET}/{thumbnail}")
