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
