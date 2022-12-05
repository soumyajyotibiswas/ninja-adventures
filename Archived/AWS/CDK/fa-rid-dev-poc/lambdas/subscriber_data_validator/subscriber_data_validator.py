"""
Validates the incoming request from the API gateway to perform
SELECT, UPDATE, DELETE OR INSERT in the `${appName}-subscriber-application-table-${stage}` DDB table
"""

import json
from typing import Dict, Union

from incoming_data_schema import SCHEMA
from jsonschema import exceptions, validate


def validate_json_schema(json) -> Union[bool,str]:
    """_summary_

    Args:
        json (_type_): _description_

    Returns:
        bool | str: _description_
    """
    try:
        if validate(json,SCHEMA) is None:
            return True
    except exceptions.ValidationError as err:
        return str(err.message)


def lambda_hander(event,context) -> Dict:
    """_summary_

    Args:
        event (_type_): _description_
        context (_type_): _description_

    Returns:
        _type_: _description_
    """
    validation_result = validate_json_schema(json.loads(event['body']))
    if isinstance(validation_result,bool):
        status_code = 200
        body = 'Hello World!'
    else:
        status_code = 200
        body = validation_result
    return {
        "isBase64Encoded": False,
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(body)
    }
