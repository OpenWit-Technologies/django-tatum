"""Utilities used in django tatum."""
import json

from typing import Any

from django_tatum.apps.tatum.tatum_client import creds
from django_tatum.apps.tatum.tatum_client.types.currencies import FiatAndCryptoCurrency
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


def check_base_pair_currency_supported(basePair: str):
    """Check that the currency is supported

    Args:
        basePair (str): Base pair currency to be validated.

    Returns:
        bool: True if the base pair currency is supported
    """
    if hasattr(FiatAndCryptoCurrency, basePair):
        print(f"{basePair} is a valid currency.")
        return False
    else:
        print(f"{basePair} is not a valid currency.")
        return True


def validate_or_modify_currency_name(name: str):
    """Validate that a currency name has VC_ prepended.
    If VC_ is not prepended, prepend a `VC_` to the name.

    Args:
        name (str): Name of the virtual currency

    Returns:
        name (str): Returns the name of the validated virtual currency.
    """
    if len(name) > 30:
        raise ValueError("name value cannot be more than 30 characters")
    if len(name) >= 28 and not name.startswith("VC_"):
        raise ValueError("Name character length must be less than 28 if not prepended with `VC_`. Please provide a shorter name.")
    if len(name) <= 27 and not name.startswith("VC_"):
        if name.startswith("vc_"):
            name = name.replace("vc_", "VC_", 1)
        else:
            name = f"VC_{name}"
    return name
