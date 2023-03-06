"""_summary_

Returns:
    _type_: _description_
"""

import logging

import boto3

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] (%(levelname)s) [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z"
)
logger = logging.getLogger()


def lambda_handler(event,context):
    """_summary_

    Args:
        event (_type_): _description_
        context (_type_): _description_

    Returns:
        _type_: _description_
    """
    return "hello world!"

