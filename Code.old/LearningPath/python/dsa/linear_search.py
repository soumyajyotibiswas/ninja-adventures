import boto3
from boto3.dynamodb.conditions import Key
from utils import generate_pdf


def get_products(region: str) -> list:
    """gets products

    Args:
        region (str): input region

    Returns:
        list: product list
    """

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("products")
    results = table.scan()
    if "Items" in results and len(results["Items"]) != 0:
        return [
            Item["product_name"]
            for Item in results["Items"]
            if Item["region"] == region
        ]


def handler(event: dict, context):
    """Main handler

    Args:
        event (dict): input event
        context (_type_): input context

    Returns:
        json: lambda response
    """
    if (
        event is None
        or "queryStringParameters" not in event
        or len(event["queryStringParameters"]) == 0
        or "region" not in event["queryStringParameters"]
        or len(event["queryStringParameters"]["region"]) == 0
        or event["queryStringParameters"]["region"].lower() not in ["us", "eur", "apac"]
    ):
        return {"statusCode": 400}

    region_from_event = event["queryStringParameters"]["region"].lower()
    product_list = get_products(region_from_event)
    encoded_string = generate_pdf(product_list)
    return {
        "statusCode": 200,
        "isBase64Encoded": True,
        "body": encoded_string,
        "headers": {
            "Content-Type": "application/pdf",
            "Content-Disposition": "attachment; filename=report.pdf",
        },
    }
