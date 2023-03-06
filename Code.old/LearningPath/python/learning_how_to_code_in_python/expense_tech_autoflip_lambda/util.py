import dateutil.parser


# boiler plate response structure
def respond(statuscode, body, is_json=False):
    return {
        "statusCode": statuscode,
        "headers": {"Content-Type": "application/json"},
        "body": body,
        "isBase64Encoded": False,
    }


# validate's that the supplied value is a valid iso datetime
def validate_time(value):
    try:
        dateutil.parser.isoparse(value)
        return True
    except Exception as e:
        print("Exception :", e)
        return False


# converts a dictionary's keys to lower case
def lower_dict(d):
    return d if d is None else dict((k.lower(), v) for k, v in d.items())
