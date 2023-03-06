import base64
import os

import expense_tech_autoflip_lambda.sim2 as sim2
from expense_tech_autoflip_lambda.util import respond, validate_time

EXPENSE_RESOLVER_GROUP = os.environ["Expense_resolver_group"]


# query ticket(s) based on parameters
def api_query(request):
    id = None
    created_since = None
    modified_since = None

    if request.method != "get":
        return respond(405, "Method must be GET")

    # assign parameters to variables and perform basic validation
    # note: if no parameters supplied we will return all open tickets
    if request.parameters is not None:
        if len(request.parameters) != 1:
            return respond(400, "Only 1 parameter is allowed")

        for key, value in request.parameters.items():
            if key == "id":
                id = value
            elif key == "createdsince":
                created_since = value
            elif key == "modifiedsince":
                modified_since = value
            else:
                return respond(400, f"Invalid parameter: {key}")

        # validate datetime parameters
        if created_since is not None and not validate_time(created_since):
            return respond(400, "Invalid datetime format for parameter: CreatedSince")

        if modified_since is not None and not validate_time(modified_since):
            return respond(400, "Invalid datetime format for parameter: ModifiedSince")

    sim_client = sim2.SIMClient()

    # create query filter
    if id is not None:  # specific issue by id
        return sim_client.get_issue(id)
    elif created_since is not None:  # all open issues created since
        query = f'extensions.tt.assignedGroup:("{EXPENSE_RESOLVER_GROUP}") AND extensions.tt.rootCause:("Direct Employee created TT") AND createDate:[{created_since} TO NOW]'
    elif modified_since is not None:  # all issues modified since regardless of status
        query = f'extensions.tt.assignedGroup:("{EXPENSE_RESOLVER_GROUP}") AND lastUpdatedDate:[{modified_since} TO NOW]'
    else:  # all open issues
        query = (
            f'extensions.tt.assignedGroup:("{EXPENSE_RESOLVER_GROUP}") AND status:Open'
        )

    # send query to maxis and return response
    return sim_client.search(query)


# get edits for ticket
def api_edits(request):
    id = None

    if request.method != "get":
        return respond(405, "Method must be GET")

    if request.parameters is None:
        return respond(400, "Parameter required")

    # assign parameters to variables
    for key, value in request.parameters.items():
        if key == "id":
            id = value
        else:
            return respond(400, f"Invalid parameter: {key}")

    sim_client = sim2.SIMClient()
    return sim_client.get_edits(id)


# edit/update ticket based on request
def api_edit(request):
    id = None

    if request.method != "post":
        return respond(405, "Method must be POST")

    if not request.content_type.__contains__("application/json"):
        return respond(415, "Content-Type must be application/json")

    if request.parameters is None:
        return respond(400, "Parameter required")

    if request.body is None:
        return respond(400, "No request")

    for key, value in request.parameters.items():
        if key == "id":
            id = value
        else:
            return respond(400, f"Invalid parameter: {key}")

    if id is None:
        return respond(400, "Missing required parameter: id")

    if request.is_base64_encoded:
        print("Yes")
        content = base64.b64decode(request.body).decode("utf-8")
    else:
        content = request.body

    # post edit json to maxis
    sim_client = sim2.SIMClient(
        on_behalf_of=request.on_behalf_of, effective_date=request.effective_date
    )
    return sim_client.post_edits(id, content)


# create thread based on payload
def api_thread(request):
    # id = None

    if request.method != "post":
        return respond(405, "Method must be POST")

    if not request.content_type.__contains__("application/json"):
        return respond(415, "Content-Type must be application/json")

    if request.parameters is not None:
        return respond(400, "No parameters allowed")

    if request.body is None:
        return respond(400, "No request")

    if request.is_base64_encoded:
        content = base64.b64decode(request.body).decode("utf-8")
    else:
        content = request.body

    # post edit json to maxis
    sim_client = sim2.SIMClient(
        on_behalf_of=request.on_behalf_of, effective_date=request.effective_date
    )
    return sim_client.post_thread(content)


# edit/update ticket thread based on request
def api_thread_edit(request):
    thread_id = None

    if request.method != "post":
        return respond(405, "Method must be POST")

    if not request.content_type.__contains__("application/json"):
        return respond(415, "Content-Type must be application/json")

    if request.parameters is None:
        return respond(400, "Parameter required")

    if request.body is None:
        return respond(400, "No request")

    for key, value in request.parameters.items():
        if key == "threadid":
            thread_id = value
        else:
            return respond(400, f"Invalid parameter: {key}")

    if id is None:
        return respond(400, "Missing required parameter: threadid")

    if request.is_base64_encoded:
        content = base64.b64decode(request.body).decode("utf-8")
    else:
        content = request.body

    # post edit json to maxis
    sim_client = sim2.SIMClient(
        on_behalf_of=request.on_behalf_of, effective_date=request.effective_date
    )
    return sim_client.post_thread_edits(thread_id, content)


# attach file to ticket
def api_attach(request):
    id = None
    filename = None

    if request.method != "post":
        return respond(405, "Method must be POST")

    if request.body is None:
        return respond(400, "No request")

    for key, value in request.parameters.items():
        if key == "id":
            id = value
        elif key == "filename":
            filename = value
        else:
            return respond(400, f"Invalid parameter: {key}")

    if id is None:
        return respond(400, "Missing required parameter: id")

    if filename is None:
        return respond(400, "Missing required parameter: filename")

    if filename.__contains__("/") or filename.__contains__("\\"):
        return respond(400, "Filename cannot include path")

    if not filename.__contains__(".") or filename.endswith("."):
        return respond(400, "Filename must include extension")

    # decode contents if necessary
    if request.is_base64_encoded:
        data = base64.b64decode(request.body)
    else:
        data = request.body

    # attach the file and return response
    sim_client = sim2.SIMClient(
        on_behalf_of=request.on_behalf_of, effective_date=request.effective_date
    )
    return sim_client.attach_file(id, filename, data, request.content_type)
