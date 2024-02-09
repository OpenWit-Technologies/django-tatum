from django_tatum.apps.tatum.tatum_client.virtual_accounts.base import BaseRequestHandler


class LedgerFees(BaseRequestHandler):
    def __init__(self):
        """Initialize TatumVirtualCurrency class."""
        self.setup_request_handler("blockchain/")
        super().__init__()

    def estimate_ledger_to_blockchain_transaction_fees(self, sender_account_id: str, address: str,):
        pass
