import json

import sim
from expense_tech_autoflip_lambda.util import respond

# extends the functionality of "SIMClient" class
# https://gitlab.aws.dev/wwps-proserve-edu-slg/sim-client-python
# methods have been modified to return error responses from MAXIS


class SIMClient(sim.SIMClient):
    def __init__(self, auth="iam", on_behalf_of=None, effective_date=None):
        """
        Construct an instance of the class.

        :param auth: 'midway' to use Midway auth or 'iam' to use current IAM role for auth
        :param on_behalf_of: the full identity of the individual on which the request is on behalf of
        :param effective_date: the timestamp at which the edit should be applied
        """
        super().__init__(auth)
        if on_behalf_of is not None:
            self._session.headers["Amzn-OnBehalfOf"] = on_behalf_of
        if effective_date is not None:
            self._session.headers["Amzn-EffectiveDate"] = effective_date

    def _get(self, path, params={}):
        """
        Execute a SIM API get call.

        :param path: API endpoint to call
        :param params: query parameters to add to call, defaults to none
        :return: parsed response as either a dictionary or list
        """
        self._check_token()
        url = f"{self._sim_url}/{path}"
        print(url, params)
        response = self._session.get(url, params=params)
        print(response.text)
        # response.raise_for_status() we don't want to raise the error. we are returning errors directly from maxis
        try:
            return respond(response.status_code, response.json(), is_json=True)
        except ValueError:
            return respond(response.status_code, response.text, is_json=False)

    def _post(self, path, body, file=None):
        """
        Execute a SIM API post call.

        :param path: API endpoint to call
        :param body: dictionary to send to endpoint
        :return: ID of created resource
        """
        self._check_token()
        url = f"{self._sim_url}/{path}"
        response = self._session.post(url, json=body, files=file)
        # response.raise_for_status() we don't want to raise the error. we are returning errors directly from maxis

        try:
            return respond(response.status_code, response.json(), is_json=True)
        except ValueError:
            return respond(response.status_code, response.text, is_json=False)

    def get_issue(self, issue_id):
        """
        Get a single issue.

        :param issue_id: identifier or alias of desired issue
        :return: dictionary of issue data
        """
        path = f"issues/{issue_id}"
        return self._get(path)

    def search(self, query):
        """
        Search for issues within SIM.

        :param query: SOLR-formatted search query
        :return: list of search results
        """
        path = "issues"
        params = {"q": query, "sort": "id"}
        documents = []
        while True:
            response = self._get(path, params)
            if response["statusCode"] == 200:
                documents.extend(response["body"]["documents"])
                params["startToken"] = response["body"].get("startToken")
                if not params["startToken"]:
                    return respond(200, documents, is_json=False)
            else:
                return response

    def get_edits(self, issue_id):
        """
        Get all edits for issue.

        :param issue_id: identifier or alias of desired issue
        :return: dictionary of edit data
        """
        path = f"issues/{issue_id}/edits"
        return self._get(path)

    # post edits from json payload directly

    def post_edits(self, issue_id, payload):
        if isinstance(payload, str):
            edits = json.loads(payload)
        elif not isinstance(payload, dict):
            return respond(400, "Invalid payload.")
        else:
            edits = payload

        print(issue_id)
        print(edits)
        return self._post(f"issues/{issue_id}/edits", edits)

    # post create thread json payload directly

    def post_thread(self, payload):
        if isinstance(payload, str):
            edits = json.loads(payload)
        elif not isinstance(payload, dict):
            raise Exception("Invalid payload.")
        else:
            edits = payload

        return self._post("threads", edits)

    # post thread edits from json payload directly

    def post_thread_edits(self, thread_id, payload):
        if isinstance(payload, str):
            edits = json.loads(payload)
        elif not isinstance(payload, dict):
            raise Exception("Invalid payload.")
        else:
            edits = payload

        return self._post(f"threads/{thread_id}/edits", edits)

    # attach a file to an issue

    def attach_file(self, issue_id, filename, data, content_type):
        # attachment endpoint doesn't work with aliases
        # if the id is not the guid try to resolve it automatically
        if len(issue_id) < 20:
            response = self.get_issue(issue_id)
            if response["statusCode"] == 200:
                issue_id = response["body"]["id"]
            else:
                return response

        file = {"file": (filename, data, content_type)}
        return self._post(f"issues/{issue_id}/attachments", body=None, file=file)
