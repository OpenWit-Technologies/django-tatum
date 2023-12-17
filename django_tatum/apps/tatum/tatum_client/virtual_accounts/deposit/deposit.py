from django_tatum.apps.tatum.tatum_client.virtual_accounts.base import BaseRequestHandler
from django_tatum.apps.tatum.utils.response_handlers import handle_response_object


class Deposit(BaseRequestHandler):
    def __init__(self):
        """Initialize TatumVirtualCurrency class."""
        self.setup_request_handler("ledger/deposits")
        super().__init__()

    def list_all_deposits_for_product(
        self,
        page_size: int = None,
        page: int = None,
        sort: str = None,
        status: str = None,
        currency: str = None,
        transaction_id: str = None,
        to: str = None,
        account_id: str = None,
    ):
        """List all deposits for a product.

        Args:
            page_size (int, optional) <= 50: Number of records per page. Max number of items per page is 50. Defaults to None.
            page (int, optional): Page number. Defaults to None.
            sort (str, optional): Direction of sorting. Can be asc or desc. Enum: "asc" "desc".
                Defaults to None.
            status (str, optional): Deposit status.  Enum: "Done" "InProgress". Defaults to None.
            currency (str, optional): Filter by currency. Defaults to None.
            transaction_id (str, optional): filter by transaction ID. Defaults to None.
            to (str, optional): filter by "to" address. Defaults to None.
            account_id (str, optional): Filter by account ID. Defaults to None.

        Returns:
            [type]: [description]
        """
        query: dict = {}

        if page_size:
            query["pageSize"] = page_size
        if page:
            query["page"] = page
        if sort:
            query["sort"] = sort
        if status:
            query["status"] = status
        if currency:
            query["currency"] = currency
        if transaction_id:
            query["txId"] = transaction_id
        if to:
            query["to"] = to
        if account_id:
            query["accountId"] = account_id

        response: str = handle_response_object(self.Handler.get(params=query))
        return response

    def count_of_found_entities_for_get_deposit_request(
        self,
        page_size: int = None,
        page: int = None,
        sort: str = None,
        status: str = None,
        currency: str = None,
        transaction_id: str = None,
        to: str = None,
        account_id: str = None,
    ):
        """Count of found entities for get deposit request.

        Args:
            page_size (int, optional) <= 50: Number of records per page. Max number of items per page is 50. Defaults to None.
            page (int, optional): Page number. Defaults to None.
            sort (str, optional): Direction of sorting. Can be asc or desc. Enum: "asc" "desc".
                Defaults to None.
            status (str, optional): Deposit status.  Enum: "Done" "InProgress". Defaults to None.
            currency (str, optional): Filter by currency. Defaults to None.
            transaction_id (str, optional): filter by transaction ID. Defaults to None.
            to (str, optional): filter by "to" address. Defaults to None.
            account_id (str, optional): Filter by account ID. Defaults to None.

        Returns:
            [type]: [description]
        """
        query: dict = {}

        if page_size:
            query["pageSize"] = page_size
        if page:
            query["page"] = page
        if sort:
            query["sort"] = sort
        if status:
            query["status"] = status
        if currency:
            query["currency"] = currency
        if transaction_id:
            query["txId"] = transaction_id
        if to:
            query["to"] = to
        if account_id:
            query["accountId"] = account_id

        self.Handler.url += "/count"

        response: str = handle_response_object(self.Handler.get(params=query))
        return response
