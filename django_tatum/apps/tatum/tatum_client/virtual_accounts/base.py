from django_tatum.apps.tatum.tatum_client import creds
from django_tatum.apps.tatum.utils.requestHandler import RequestHandler


class BaseRequestHandler:
    def __init__(self):
        self.url_prefix: str = ""
        self.Handler: RequestHandler = None  # Initialize the handler as None

    def setup_request_handler(self, url_prefix) -> RequestHandler:
        self.url_prefix = url_prefix
        self.requestUrl = f"{creds.TATUM_BASE_URL}{url_prefix}"
        self.Handler = RequestHandler(
            self.requestUrl,
            {
                "Content-Type": "application/json",
                "x-api-key": creds.TATUM_API_KEY,
            },
        )

        return self.Handler

    def extracted_from_send_payment(self, arg0, data):
        self.setup_request_handler(arg0)
        response = self.Handler.post(data)
        return response.json()
