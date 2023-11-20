from django_tatum.apps.tatum.utils.utility import write_json_to_file
from requests import Response
from typing import Union

from django_tatum.apps.tatum.tatum_client.virtual_accounts.account import TatumVirtualAccounts

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


    def get_customer_details(
        self, 
        customer_id: str
    ):
        self.setup_request_handler(f"ledger/customer/{customer_id}")
        response = self.Handler.get()
        return response.json()

    def update_customer(
        self,
        customer_id: str,
        externalId: str,
        accountingCurrency: str,
        customerCountry: str,
        providerCountry: str,
    ):
        self.setup_request_handler(f"ledger/customer/{customer_id}")

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
    
    def _activate_all_customer_virtual_accounts(self, customer_account_list):
        for customer_account in customer_account_list:
            tva = TatumVirtualAccounts()
            response = tva.activate_account(account_id=customer_account["id"])
            print(response)
        return "All accounts have been deactivated."
    
    def activate_customer(
        self, 
        customer_id:str,
    ) -> dict[str, Union[str, int]]:
        
        if customer_account_list := self._get_all_customer_virtual_accounts(
            customer_id=customer_id
        ):
            # activate all customer accounts
            self._activate_all_customer_virtual_accounts(customer_account_list=customer_account_list)
        
        self.setup_request_handler (f"ledger/customer/{customer_id}/activate")
        response: Response = self.Handler.put() 
        if response.status_code == 204:
            response_object: dict[str, str] = {
                "message": "Activated successfully.",
                "status_code": 204,
            }
            return response_object
        return response.json()   
    
    
    def _get_all_customer_virtual_accounts(self, customer_id):
        tva = TatumVirtualAccounts()
        customer_account_list: list[dict] = tva.list_all_customer_accounts(customer_id=customer_id) 
        if "statusCode" in customer_account_list:
            return []
        
        else :
        # return only the customer accounts that have active: true
        #customer_account_list = [customer_account for customer_account in customer_account_list if customer_account["active"] == True]
        # return customer_account_list
            # Separate active and inactive accounts using if-else statement
            active_customer_accounts = [customer_account for customer_account in customer_account_list if customer_account["active"]]
            print(active_customer_accounts)
            write_json_to_file(filename="active_customer_accounts.json", response=active_customer_accounts)
            return active_customer_accounts
    
    def _deactivate_all_customer_virtual_accounts(self, customer_account_list):
        for customer_account in customer_account_list:
            tva = TatumVirtualAccounts()
            response = tva.deactivate_account(account_id=customer_account["id"])
            print(response)
        return "All accounts have been deactivated."
    
    def deactivate_customer(
        self, 
        customer_id:str,
    ) -> dict[str, str]:
        
        if customer_account_list := self._get_all_customer_virtual_accounts(
            customer_id=customer_id
        ):
            # deactivate all customer accounts
            self._deactivate_all_customer_virtual_accounts(customer_account_list=customer_account_list)
        
        self.setup_request_handler (f"ledger/customer/{customer_id}/deactivate")
        response: Response = self.Handler.put() 
        if response.status_code == 204:
            response_object: dict[str, str] = {
                "message": "Deactivated successfully.",
                "status_code": 204,
            }
            return response_object
        return response.json()           
    
    def enable_customer(
        self, 
        customer_id:str,
    ) -> dict[str, str]:
        self.setup_request_handler (f"ledger/customer/{customer_id}/enable")
        response: Response = self.Handler.put() 
        if response.status_code == 204:
            response_object: dict[str, str] = {
                "message": "Enabled successfully.",
                "status_code": 204,
            }
            return response_object
        return response.json()      
    
    def disable_customer(
        self, 
        customer_id:str,
    ) -> dict[str, str]:
        self.setup_request_handler (f"ledger/customer/{customer_id}/disable")
        response: Response = self.Handler.put() 
        if response.status_code == 204:
            response_object: dict[str, str] = {
                "message": "Disabled successfully.",
                "status_code": 204,
            }
            return response_object
        return response.json()        



if __name__ == "__main__":
    tac = TatumCustomer()
    # print(tac.list_all_customers())
    # print(tac.get_customer_details(customer_id="653307d18c610c9e0ef45940"))
    
    # print(
    #     tac.update_customer(
    #         customer_id= "653307d18c610c9e0ef45940",
    #         externalId= "987654321",
    #         accountingCurrency= "USD",
    #         customerCountry= "US",
    #         providerCountry = "GB"
    #     )
    # )
    
    # print(tac.activate_customer(customer_id = "653307d18c610c9e0ef45940"))
    print(tac.deactivate_customer(customer_id = "653307d18c610c9e0ef45940"))
    # print(tac.enable_customer(customer_id = "653307d18c610c9e0ef45940"))
    # print(tac.disable_customer(customer_id = "653307d18c610c9e0ef45940"))
