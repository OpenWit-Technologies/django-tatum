from django_tatum.apps.tatum.tatum_client import creds
from django_tatum.apps.tatum.utils.requestHandler import RequestHandler


class TatumVirtualAccounts:
    def __init__(self):
        self.requestUrl = f"{creds.TATUM_BASE_URL}ledger/account"
        self.Handler = RequestHandler(
            self.requestUrl,
            {
                "Content-Type": "application/json",
                "x-api-key": creds.TATUM_API_KEY,
            },
        )

    def generate_virtual_account(self, data: dict):
        response = self.Handler.post(data)
        return response.json()

    def list_all_virtual_accounts(self, query: dict = None):
        # sourcery skip: class-extract-method
        if query is None:
            query = {}
        response = self.Handler.get(params=query)
        return response.json()

    def get_account_balance(self, account_id: str):

        requestUrl = f"{creds.TATUM_BASE_URL}ledger/account/{account_id}/balance"
        Handler = RequestHandler(
            requestUrl, {"x-api-key": creds.TATUM_API_KEY}
        )

        response = Handler.get()
        return response.json()
    
    def count_account_request(self, query: dict = None):
        requestUrl = f"{creds.TATUM_BASE_URL}ledger/account/count"
        Handler = RequestHandler(
            requestUrl, 
            {"x-api-key": creds.TATUM_API_KEY}
        )
        if query is None:
            query = {}
        response = Handler.get(params=query)
        return response.json()
    
    def generate_multiple_virtual_account_in_batch(self, data:dict):
        requestUrl = f"{creds.TATUM_BASE_URL}ledger/account/batch"
        Handler = RequestHandler(
            requestUrl, 
            {"x-api-key": creds.TATUM_API_KEY}
        )
        response = Handler.post(data)
        return response.json()
    
    def list_all_customer_account(self, customer_id: str, pageSize: int):
        requestUrl = f"{creds.TATUM_BASE_URL}ledger/account/customer/{customer_id}"
        Handler = RequestHandler(
            requestUrl, 
            {"x-api-key": creds.TATUM_API_KEY}
        )
        query = {}
        if pageSize:
            query["pageSize"] = pageSize

        response = Handler.get(params=query)
        return response.json()



    
#if __name__ == "__main__":
#    tatum_virtual_account = TatumVirtualAccounts()
#    data = {"currency": "ETH",
#            "xpub": "xpub6F5FVUCZBPAogVTxdii4ymwy4rWZDXZsWFQBbSq1FiSNCzQtQffqrrie7FFXMNBrwjnv2v8Kwhs59RCteAFcQnNVUy4T3yygRYaL3DJGxZF"
#            }
#    tvc = tatum_virtual_account.generate_virtual_account(data)
#    print(tvc)

#if __name__ == "__main__":
#    tatum_virtual_account = TatumVirtualAccounts()
#    tvc = tatum_virtual_account.list_all_virtual_accounts()
#    print(tvc)
    
#if __name__ == "__main__":
#    tatum_virtual_account = TatumVirtualAccounts()
#    id = "652f090c4654e4a7feb28de4"
#    tvc = tatum_virtual_account.get_account_balance(id)
#    print(tvc)
    
#if __name__ == "__main__":
#    tatum_virtual_account = TatumVirtualAccounts()
#    tvc = tatum_virtual_account.count_account_request()
#    print(tvc)

if __name__ == "__main__":
    tatum_virtual_account = TatumVirtualAccounts()
    data = {
        "accounts":  [
            {
                "currency": "ETH"
            }
        ]
    }
    tvc = tatum_virtual_account.generate_multiple_virtual_account_in_batch(data)
    print(tvc)

#if __name__ == "__main__":
#    tatum_virtual_account = TatumVirtualAccounts()
#    customer_id = "652f090c4654e4a7feb28de4" 
#    pageSize = "5"
#    tvc = tatum_virtual_account.list_all_customer_account(customer_id, pageSize)
#    print(tvc)