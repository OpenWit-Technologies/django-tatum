"""Handles the response objects to return appropriate messages."""


import json

from dataclasses import dataclass
from typing import Any
from typing import Optional
from requests import Response


@dataclass
class CustomResponse:
    status_code: int
    response: Optional[dict] = None
    message: Optional[str] = None


def handle_response_object(
    response: Response,
    additional_message: str = None,
    custom_response: CustomResponse = None,
) -> str:
    """
    This function handles the response object returned by a request.

    Parameters:
    response (obj): The response object to be handled.

    Returns:
    obj: The handled response object.
    """
    if response.content:
        tatum_response: Any = response.json()
    else:
        tatum_response: Any = None

    response_object: dict[str, Any] = {
        "message": "",
        "status_code": 0,
        "response": {},
    }

    if response.status_code == 200:
        response_object["message"] = "Success."
        if additional_message is not None:
            response_object["message"] += f" {additional_message}"
        response_object["status_code"] = 200
        response_object["response"] = tatum_response
        return json.dumps(response_object)

    elif response.status_code == 204:
        response_object["message"] = "Success. No Content."
        if additional_message is not None:
            response_object["message"] += f" {additional_message}"
        response_object["status_code"] = 204
        return json.dumps(response_object)

    elif response.status_code == 400:
        response_object["message"] = "Bad request."
        if additional_message is not None:
            response_object["message"] += f" {additional_message}"
        response_object["status_code"] = 400
        response_object["response"] = tatum_response
        return json.dumps(response_object)

    elif response.status_code == 401:
        response_object["message"] = "Unauthorized."
        if additional_message is not None:
            response_object["message"] += f" {additional_message}"
        response_object["status_code"] = 401
        response_object["response"] = tatum_response
        return json.dumps(response_object)

    elif response.status_code == 403:
        response_object["message"] = "Forbidden."
        response_object["status_code"] = 403
        response_object["response"] = tatum_response
        return json.dumps(response_object)

    elif response.status_code == 500:
        response_object["message"] = "Internal server error."
        response_object["status_code"] = 500
        response_object["response"] = tatum_response
        return json.dumps(response_object)

    else:
        response_object["message"] = "Unknown error."
        response_object["status_code"] = 0
        response_object["response"] = tatum_response
        return json.dumps(response_object)
