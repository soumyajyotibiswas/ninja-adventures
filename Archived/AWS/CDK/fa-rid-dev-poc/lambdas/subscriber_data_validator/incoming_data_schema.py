"""
Hosting JSON schema for incoming requests
"""

SCHEMA = {
    "type": "object",
    "properties": {
        "appName": {"type":"string","pattern": "^[A-Za-z][A-Za-z0-9_-]{4,29}$"},
        "accountIds": {
            "type":"array",
            "items": {
                "type":"string",
                "pattern":'\d{12}'
            },
            "uniqueItems": True,
            "minItems ": 1
        },
        "primaryOwner": {"type":"string","pattern": "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"},
        "bindleIds": {
            "type":"array",
            "items": {"type":"string"},
            "minItems ": 1,
            "uniqueItems": True
        }
    }
}