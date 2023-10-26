from django_tatum.apps.tatum.tatum_client import creds 
from django_tatum.apps.tatum.utils.requestHandler import RequestHandler


class TatumCustomer:
    def __init__(self):
        self.requestUrl = f"{creds.TATUM_BASE_URL}ledger/customer"
        self.Handler = RequestHandler(
            self.requestUrl,
            {
                "Content-Type": "application/json",
                "x-api-key": creds.TATUM_API_KEY,
            },
        )

    def list_all_customers(self, pageSize: int, offset: int = None):
        query = {}
        if pageSize:
            query["pageSize"] = pageSize
        if offset:
            query["offset"] = offset

        response = self.Handler.get(params=query)
        return response.json()

    def get_customer_details(self, id: str):
        self.requestUrl = f"{creds.TATUM_BASE_URL}ledger/customer/{id}"
        self.Handler = RequestHandler(
            self.requestUrl,
            {"x-api-key": creds.TATUM_API_KEY},
        )

        response = self.Handler.get()
        return response.json()

    def update_customer(
        self,
        id: str,
        externalId: str,
        accountingCurrency: str = None,
        customerCountry: str = None,
        providerCountry: str = None,
    ):

        self.requestUrl = f"{creds.TATUM_BASE_URL}ledger/customer/{id}"
        self.Handler = RequestHandler(
            self.requestUrl,
            {"Content-Type": "application/json", "x-api-key": creds.TATUM_API_KEY},
        )

        payload = {
            "externalId": externalId,
            "accountingCurrency": accountingCurrency,
            "customerCountry": customerCountry,
            "providerCountry": providerCountry,
        }

        response = self.Handler.put(data=payload)
        return response.json()


    def activate_customer(self, id: str):
        response = self._activation_toggle_put_request(id, '/activate')
        return response.json()
    
    def deactivate_customer(self, id: str):
        return self._customer_id_parser(id, '/deactivate', ' deactivated successfully')

    def enable_customer(self, id: str):
        return self._customer_id_parser(id, '/enable', ' enabled successfully.')
    
    def disable_customer(self, id: str):
        return self._customer_id_parser(id, '/disable', ' disabled successfully.')

    def _customer_id_parser(self, id, url_suffix, message_suffix):
        response = self._activation_toggle_put_request(id, url_suffix)
        return f"Customer {id} {message_suffix}" if response.status == 204 else response.json()

    def _activation_toggle_put_request(self, id, url_suffix):
        requestUrl = f"{creds.TATUM_BASE_URL}ledger/customer/{id}{url_suffix}"
        Handler = RequestHandler(requestUrl, {"Content-Type": "application/json", "x-api-key": creds.TATUM_API_KEY})

        return Handler.put()
    
if __name__ == "__main__":
    tatum_customer_account = TatumCustomer()
    pageSize = 5
    offset = 0
    tca = tatum_customer_account.list_all_customers(pageSize, offset)
    print(tca)
    

