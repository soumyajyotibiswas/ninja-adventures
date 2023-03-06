import time
import uuid
from datetime import datetime, timedelta

from expense_tech_autoflip_lambda.api import api_edit, api_query
from expense_tech_autoflip_lambda.util import lower_dict, respond


# map the lambda event dictionary to a LambdaRequest class with the required fields for our API
class LambdaRequest:
    def __init__(self, event):

        ist_today = str(datetime.utcnow() + timedelta(days=0, hours=5, minutes=0))[:10]
        utc_today = str(
            (
                datetime.strptime(f"{ist_today} 00:00:00", "%Y-%m-%d %H:%M:%S")
                - timedelta(hours=5, minutes=30)
            ).strftime("%Y-%m-%d %H:%M:%S")
        )

        self.content_type = "application/json".lower()
        self.on_behalf_of = "kerberos:prernasi@ANT.AMAZON.COM"
        self.effective_date = None
        self.is_base64_encoded = False
        self.parameters = lower_dict(
            {"createdsince": utc_today[:10] + "T" + utc_today[11:] + "Z"}
        )
        self.method = "GET".lower()
        self.path = "/query".lower()
        self.body = {}


# main function that handles all incoming requests
def lambda_handler(event, context):
    try:

        request = LambdaRequest(event)

        # Get the Ticket List

        output = list(api_query(request)["body"])
        ticket_list = [i["id"] for i in output]

        # Update the tickets

        for tkt in ticket_list:

            comment_id = str(uuid.uuid4())

            request.parameters = lower_dict({"id": tkt})
            request.method = "POST".lower()
            request.path = "/edit".lower()

            request.body = {
                "pathEdits": [
                    {
                        "editAction": "PUT",
                        "path": "/conversation/" + comment_id,
                        "data": {
                            "id": comment_id,
                            "contentType": "text/plain",
                            "messageType": "conversation",
                            "message": "This CTI is not meant for Direct Employee cut TT. Correcting the CTI to Fincom for initial review",
                        },
                    }
                ]
            }
            api_edit(request)

            request.body = {
                "pathEdits": [
                    {
                        "editAction": "PUT",
                        "path": "/extensions/tt",
                        "data": {
                            "assignedGroup": "Expense-Reports-FinCom",
                            "category": "Employee and Candidate Expenses",
                            "type": "Employee Expense Submission",
                            "item": "Expense Submission Inquiry",
                            "caseType": "Trouble Ticket",
                            "impact": 5,
                        },
                    }
                ]
            }
            api_edit(request)

            request.body = {
                "pathEdits": [{"editAction": "PUT", "path": "/status", "data": "Open"}]
            }
            api_edit(request)

            time.sleep(2)

        return ticket_list

    except Exception as e:
        print("{}: {}".format(type(e).__name__, e))
        return respond(500, None)
