"""Utilities used in django tatum."""
import json

from typing import Any

from django_tatum.apps.tatum.tatum_client import creds
from django_tatum.apps.tatum.utils.requestHandler import RequestHandler


def validate_required_fields(fields: dict) -> bool:
    """
    Validates that all required fields are present in the fields dictionary.
    """
    return {
        "detail": f"Field {field} is required."
        for field in fields
        if fields.get(field) is None or fields.get(field).strip() == "" or fields.get(field) == []
    }


class AccountApi:
    def __init__(self):
        self.requestUrl = f"{creds.TATUM_BASE_URL}ledger/account"
        self.Handler = RequestHandler(
            self.requestUrl,
            {
                "Content-Type": "application/json",
                "x-api-key": creds.TATUM_API_KEY,
            },
        )


def write_json_to_file(
    filename: str,
    response: Any,
):
    """Write the dumped response to a json file.

    Args:
        filename (str): name of the output file.
        response (Any): The response.json object from the response to a request.
    """
    with open(filename, "w") as f:
        if isinstance(response, str):
            f.write(response)
        else:
            f.write(json.dumps(response, indent=4))
