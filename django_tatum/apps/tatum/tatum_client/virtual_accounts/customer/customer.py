from requests import Response
from typing import Union


from django_tatum.apps.tatum.tatum_client.virtual_accounts.account import TatumVirtualAccounts
from django_tatum.apps.tatum.tatum_client.virtual_accounts.base import BaseRequestHandler
from django_tatum.apps.tatum.utils.response_handlers import handle_response_object

from django_tatum.apps.tatum.utils.utility import write_json_to_file


class TatumCustomer(BaseRequestHandler):
    def __init__(self):
        self.Handler = self.setup_request_handler("ledger/customer")

    def list_all_customers(
        self,
        pageSize: int = 10,
        offset: int = 0,
    ):
        query: dict = {
            "pageSize": pageSize,
        }

        if offset:
            query["offset"] = offset

        response: Response = handle_response_object(self.Handler.get(params=query))
        write_json_to_file(filename="all_customers.json", response=response)
        return response

    def get_customer_details(self, customer_id: str):
        self.Handler.url += f"/{customer_id}"
        response: str = handle_response_object(self.Handler.get())
        write_json_to_file(filename=f"customer_details_{customer_id}.json", response=response)
        return response

    def update_customer(
        self,
        customer_id: str,
        externalId: str,
        accountingCurrency: str = None,
        customerCountry: str = None,
        providerCountry: str = None,
    ):
        self.Handler.url += f"/{customer_id}"

        if len(externalId) > 99:
            raise ValueError("externalId value cannot be more than 100 characters")

        payload: dict[str, str] = {"externalId": externalId}
        if accountingCurrency:
            payload["accountingCurrency"] = accountingCurrency
        if customerCountry:
            payload["customerCountry"] = customerCountry
        if providerCountry:
            payload["providerCountry"] = providerCountry

        response: str = handle_response_object(self.Handler.put(data=payload))
        return response

    def _activate_all_customer_virtual_accounts(self, customer_account_list):
        for customer_account in customer_account_list:
            tva = TatumVirtualAccounts()
            response = tva.activate_account(account_id=customer_account["id"])
            print(response)
        return "All accounts have been deactivated."

    def activate_customer(
        self,
        customer_id: str,
    ) -> dict[str, Union[str, int]]:
        if customer_account_list := self._get_all_customer_virtual_accounts(customer_id=customer_id):
            # activate all customer accounts
            print(f"{customer_account_list=}")

            account_acitvation_response: str = self._activate_all_customer_virtual_accounts(
                customer_account_list=customer_account_list,
            )
            print(account_acitvation_response)

        self.setup_request_handler(f"ledger/customer/{customer_id}/activate")
        response: str = handle_response_object(
            self.Handler.put(),
            additional_message="Customer activated successfully.",
        )

        return response

    def _get_all_customer_virtual_accounts(self, customer_id):
        tva = TatumVirtualAccounts()
        customer_account_list: list[dict] = tva.list_all_customer_accounts(customer_id=customer_id)
        if "statusCode" in customer_account_list:
            return []

        else:
            # return only the customer accounts that have active: true
            # customer_account_list = [customer_account for customer_account in customer_account_list
            # if customer_account["active"] == True]
            # return customer_account_list
            # Separate active and inactive accounts using if-else statement
            active_customer_accounts = [
                customer_account for customer_account in customer_account_list if customer_account["active"]
            ]
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
        customer_id: str,
    ) -> dict[str, str]:
        if customer_account_list := self._get_all_customer_virtual_accounts(customer_id=customer_id):
            # deactivate all customer accounts
            self._deactivate_all_customer_virtual_accounts(customer_account_list=customer_account_list)

        self.setup_request_handler(f"ledger/customer/{customer_id}/deactivate")
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
        customer_id: str,
    ) -> dict[str, str]:
        self.setup_request_handler(f"ledger/customer/{customer_id}/enable")
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
        customer_id: str,
    ) -> dict[str, str]:
        self.setup_request_handler(f"ledger/customer/{customer_id}/disable")
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
    print(tac.list_all_customers())
    # print(tac.get_customer_details(customer_id="656c8e7e6b04478256b65d24"))

    # print(
    #     tac.update_customer(
    #         customer_id="653307d18c610c9e0ef45940",
    #         externalId="987654321",
    #         accountingCurrency="GBP",
    #         customerCountry="GB",
    #         providerCountry="GB",
    #     )
    # )

    # print(tac.activate_customer(customer_id="656c8e7e6b04478256b65d24"))
    # print(tac.deactivate_customer(customer_id="656c8e7e6b04478256b65d24"))
    # print(tac.enable_customer(customer_id="653307d18c610c9e0ef45940"))
    # print(tac.disable_customer(customer_id = "653307d18c610c9e0ef45940"))
