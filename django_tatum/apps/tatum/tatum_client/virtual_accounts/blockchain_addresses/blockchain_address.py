from django_tatum.apps.tatum.tatum_client import creds
from django_tatum.apps.tatum.utils.requestHandler import RequestHandler
from django_tatum.apps.tatum.tatum_client.virtual_accounts.base import BaseRequestHandler
from django_tatum.apps.tatum.utils.response_handlers import handle_response_object


class TatumBlockchainAdress(BaseRequestHandler):
    def __init__(self):
        self.requestUrl = f"{creds.TATUM_BASE_URL}offchain/account"
        self.Handler = RequestHandler(
            self.requestUrl,
            {
                "Content-Type": "application/json",
                "x-api-key": creds.TATUM_API_KEY,
            },
        )

    def create_deposit_address(self, account_id: str):
        self.requestUrl = f"{self.requestUrl}/{account_id}/address"
        self.Handler = RequestHandler(
            self.requestUrl,
            {"x-api-key": creds.TATUM_API_KEY},
        )

        response = self.Handler.post()
        return response.json()

    # TODO: Review all methods below this
    def get_all_deposit_addresses_for_a_virtual_account(
        self,
        virtual_account_id: str,
    ):
        """Get all deposit addresses generated for a virtual account.

        Args:
            virtual_account_id (str): The ID of the virtual account to get deposit addresses.

        Returns:
            _type_: _description_
        """

        self.setup_request_handler(f"offchain/account/{virtual_account_id}/address")

        response = handle_response_object(self.Handler.get())
        return response

    def create_multiple_deposit_addresses_for_a_virtual_account(
        self,
        addresses: list[str, int],
    ):
        """Create multiple deposit addresses for a virtual account.

        Args:
            addresses (list[str, int]): List of addresses to create.

        Returns:
            _type_: _description_
        """

        self.setup_request_handler("offchain/account/address/batch")

        response = handle_response_object(self.Handler.post(data=addresses))
        return response

    def check_virtual_account_assignment_to_blockchain_address(
        self,
        currency: str,
        address: str,
        index: int,
    ):
        """Check if virtual account is assigned to blockchain address.

        Args:
            currency (str): Currency to check for.
            address (str): Address to check for.
            index (int): Index to check for.

        Returns:
            _type_: _description_
        """

        self.setup_request_handler(f"offchain/account/address/{address}/{currency}")
        query: dict = {}

        if index:
            query = {"index": index}

        response = handle_response_object(self.Handler.get(query=query))
        return response

    def assign_blockchain_address_to_a_virtual_account(self, virtual_account_id: str, address: str, index: int,):
        """Assign blockchain address to a virtual account.

        Args:
            virtual_account_id (str): The ID of the virtual account to assign the address to.
            address (str): The address to assign.
            index (int): The index to assign.

        Returns:
            _type_: _description_
        """

        self.setup_request_handler(f"offchain/account/{virtual_account_id}/address/{address}")

        if index:
            query = {"index": index}

        response = handle_response_object(self.Handler.post(query=query))
        return response

    def remove_deposit_address_from_a_virtual_account(self, virtual_account_id: str, address: str, index: int,):
        """Remove deposit address from a virtual account.

        Args:
            virtual_account_id (str): The ID of the virtual account to remove the address from.
            address (str): The address to remove.
            index (int): The index to remove.

        Returns:
            _type_: _description_
        """

        self.setup_request_handler(f"offchain/account/{virtual_account_id}/address/{address}")

        if index:
            query = {"index": index}

        response = handle_response_object(self.Handler.delete(query=query))
        return response


if __name__ == "__main__":
    tatum_blockchain_address = TatumBlockchainAdress()
    account_id = "656cbfa574d8e8cd7f1db8ad"
    tba = tatum_blockchain_address.create_deposit_address(account_id)
    print(tba)
