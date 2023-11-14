<<<<<<< Updated upstream
from tatum_client import creds
from utils.requestHandler import RequestHandler
=======
# from django_tatum.apps.tatum.tatum_client import creds 
# from django_tatum.apps.tatum.utils.requestHandler import RequestHandler
from requests import Response
>>>>>>> Stashed changes

from django_tatum.apps.tatum.tatum_client.virtual_accounts.base import (
    BaseRequestHandler,
)

from django_tatum.apps.tatum.tatum_client.types.customer_types import (
    UpdateCustomerDict,
)

class TatumCustomer(BaseRequestHandler):
    def __init__(self):
        self.setup_request_handler("ledger/customer")
        super().__init__()

    def list_all_customers(
        self, 
        pageSize: int = 10, 
        offset: int = 0,
    ):
        self.setup_request_handler("ledger/customer")
          
        query: dict = {
            "pageSize": pageSize,
        }

        if offset:
            query["offset"] = offset

        response: Response = self.Handler.get(params=query)
        print(response)
        return response.json()


    def get_customer_details(self, id: str):
        self.setup_request_handler(f"ledger/customer/{id}")
        response = self.Handler.get()
        return response.json()

    def update_customer(
        self,
        id: str,
        externalId: str,
        accountingCurrency: str,
        customerCountry: str,
        providerCountry: str,
    ):
        self.setup_request_handler(f"ledger/customer/{id}")

        payload: UpdateCustomerDict = {
            "externalId": externalId,
            "accountingCurrency": accountingCurrency,
            "customerCountry": customerCountry,
            "providerCountry": providerCountry,
        }

        response: Response = self.Handler.put(
            data=payload,
        )
        return response.json()


    # def activate_customer(self, id: str):
    #     response = self.setup_request_handler(f"ledger/customer/{id}/activate")
    #     return response.json()
    
    def activate_customer(self, id: str):
         return self._customer_id_parser(id, '/activate', ' activated successfully.')
  
    
    def deactivate_customer(self, id: str):
        return self._customer_id_parser(id, '/deactivate', ' deactivated successfully')

    def enable_customer(self, id: str):
        return self._customer_id_parser(id, '/enable', ' enabled successfully.')
    
    def disable_customer(self, id: str):
        return self._customer_id_parser(id, '/disable', ' disabled successfully.')
    
    def _customer_id_parser(self, id,  message_suffix):
        response = self.setup_request_handler(f"ledger/customer/{id}")
        return f"Customer {id} {message_suffix}" if response.status == 204 else response.json()

    # def _customer_id_parser(self, id, url_suffix, message_suffix):
    #     response = self._activation_toggle_put_request(id, url_suffix)
    #     return f"Customer {id} {message_suffix}" if response.status == 204 else response.json()

    def _activation_toggle_put_request(self, id, url_suffix):
        requestUrl = f"{creds.TATUM_BASE_URL}ledger/customer/{id}{url_suffix}"
        Handler = RequestHandler(requestUrl, {"Content-Type": "application/json", "x-api-key": creds.TATUM_API_KEY})

        return Handler.put()
    
    

if __name__ == "__main__":
    tac = TatumCustomer()
    # print(tac.list_all_customers())
    # print(tac.get_customer_details(id="653307d18c610c9e0ef45940"))
    
    # print(
    #     tac.update_customer(
    #         id= "653307d18c610c9e0ef45940",
    #         externalId= "987654321",
    #         accountingCurrency= "USD",
    #         customerCountry= "US",
    #         providerCountry = "GB"
    #     )
    # )
    
    print(tac.activate_customer(id = "653307d18c610c9e0ef45940"))
