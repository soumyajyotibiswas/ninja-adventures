"""_summary_
"""
import json


def lambda_handler(event,context):
    """_summary_

    Args:
        event (_type_): _description_
        context (_type_): _description_
    """
    print("Printing event:\n",event)
    print("Printing context:\n",context)
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps("Hello World!")
    }
