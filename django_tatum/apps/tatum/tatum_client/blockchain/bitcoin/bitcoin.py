from enum import Enum
from typing import Mapping, Any

from django_tatum.apps.tatum.tatum_client import creds
from django_tatum.apps.tatum.utils.requestHandler import RequestHandler


class TransactionType(Enum):
    """Represents the type of Bitcoin transaction: incoming or outgoing."""

    OUTGOING = "outgoing"
    INCOMING = "incoming"


class BitcoinWallet:
    """Provides tools for interacting with the Bitcoin blockchain through Tatum API.

    This class offers functionalities for:

    * Creating wallets, addresses, and private keys.
    * Retrieving blockchain information (balance, blocks, transactions).
    * Managing transactions (sending, broadcasting, retrieving).

    It utilizes the Tatum API to access the Bitcoin network.

    Attributes:
        requestUrl (str): Base URL for Tatum API endpoint for Bitcoin functionality.
        Handler (RequestHandler): An instance of RequestHandler class for managing HTTP requests.
    """

    def __init__(self) -> None:
        """Initializes the BitcoinWallet object.

        Sets the base URL for Tatum API and initializes the RequestHandler object.
        """
        self.requestUrl = f"{creds.TATUM_BASE_URL}bitcoin/wallet"
        self.Handler = RequestHandler(
            self.requestUrl,
            {
                "Content-Type": "application/json",
                "x-api-key": creds.TATUM_API_KEY,
            },
        )

    def generate_wallet(self) -> Mapping[str, Any]:
        """Creates a new Bitcoin wallet on the Tatum platform.

        This method utilizes the Tatum API to interact with the Bitcoin blockchain and
        create a new wallet for you. The returned dictionary contains information
        about the created wallet, including its address, private key, and other details.

        Returns:
            Mapping[str, Any]: A dictionary containing information about the created wallet.
        """

        response = self.Handler.get()
        return response.json()

    def generate_address(self, xpub: str, *, index: int = 0) -> Mapping[str, Any]:
        """Generates a new Bitcoin address associated with the given xpub key.

        This method allows you to generate new Bitcoin addresses associated with
        an existing extended public key (xpub). You can optionally specify an index
        to control the derivation path of the generated address.

        Args:
            xpub (str): Extended public key for the wallet.
            index (int, optional): Index of the address to generate. Defaults to 0.

        Returns:
            Mapping[str, Any]: A dictionary containing information about the generated address.
        """

        self.Handler.url = f"{creds.TATUM_BASE_URL}bitcoin/address/{xpub}/{index}"
        response = self.Handler.get()
        return response.json()

    def generate_private_key(self, mnemonic: str, index: int = 0) -> Mapping[str, Any]:
        """Generates a private key based on the provided mnemonic phrase and index.

        This method uses a mnemonic phrase and an optional index to derive a new
        Bitcoin private key. The mnemonic phrase acts as a secure backup for your
        private keys.

        Args:
            mnemonic (str): Mnemonic phrase used to generate the private key.
            index (int, optional): Index of the private key to generate. Defaults to 0.

        Returns:
            Mapping[str, Any]: A dictionary containing the generated private key.
        """

        self.Handler.url = f"{creds.TATUM_BASE_URL}bitcoin/wallet/priv"
        payload = {"index": index, "mnemonic": mnemonic}
        response = self.Handler.post(data=payload)
        return response.json()

    def get_blockchain_info(self) -> Mapping[str, Any]:
        """Retrieves general information about the Bitcoin blockchain.

        This method fetches various details about the Bitcoin blockchain from the
        Tatum API, such as the current block height, difficulty, network hash rate,
        and more.

        Returns:
            Mapping[str, Any]: A dictionary containing various blockchain info.
        """

        self.Handler.url = f"{creds.TATUM_BASE_URL}bitcoin/info"
        response = self.Handler.get()
        return response.json()

    def get_hash_block(self, block_no: int) -> Mapping[str, Any]:
        """Retrieves information about a specific Bitcoin block by its block number.

        This method allows you to query information about a specific block on the
        Bitcoin blockchain using its block number. The returned dictionary contains
        details like block hash, timestamp, transactions, and more.

        Args:
            block_no (int): Block number to query.

        Returns:
            Mapping[str, Any]: A dictionary containing details about the specified block.
        """

        self.Handler.url = f"{creds.TATUM_BASE_URL}bitcoin/block/hash/{block_no}"
        response = self.Handler.get()
        return response.json()

    def get_balance(self, address: str) -> Mapping[str, Any]:
        """Retrieves the current balance of a Bitcoin address.

        Args:
            address (str): The Bitcoin address to query.

        Returns:
        Mapping: A dictionary containing information about the address balance,
            including its `balance` in satoshis and other details depending on the Tatum API response.
        """
        self.Handler.url = f"{creds.TATUM_BASE_URL}bitcoin/address/balance/{address}"
        response = self.Handler.get()
        return response.json()

    def batch_get_balance(self, addresses: list[str] | None = None) -> Mapping[str, Any]:
        """Retrieves the balance of multiple Bitcoin addresses in a single request.

        Args:
            addresses (list[str], optional): List of Bitcoin addresses to query. Defaults to None.

        Returns:
            Mapping: A dictionary where keys are addresses and values are their balances in satoshis.

        Raises:
            #   TODO: If no addresses are provided.
        """
        if not addresses:
            raise ValueError("No addresses provided")  # TODO: handle exception gracefully

        self.Handler.url = f"{creds.TATUM_BASE_URL}bitcoin/address/balance/batch"
        query_param = {"addresses": ",".join(addresses)}
        response = self.Handler.get(params=query_param)
        return response.json()

    def get_all_transactions(
        self,
        address: str,
        *,
        block_from: int,
        block_to: int,
        page_size: int = 10,
        offset: int = 0,
        txn_type: TransactionType = TransactionType.INCOMING,
    ) -> Mapping[str, Any]:
        """Retrieves all transactions associated with a Bitcoin address within a specified block range.

        Args:
            address (str): The Bitcoin address to query.
            block_from (int): Starting block number for the search.
            block_to (int): Ending block number for the search.
            page_size (int, optional): Number of transactions per page. Defaults to 10.
            offset (int, optional): Offset for pagination. Defaults to 0.
            txn_type (TransactionType, optional): Type of transactions to filter (incoming or outgoing).
                Defaults to TransactionType.INCOMING.

        Returns:
            Mapping: A dictionary containing paginated transaction data for the specified criteria,
                including information about each transaction (e.g., amount, timestamp, type).

        Raises:
            requests.exceptions.RequestException: If an error occurs during the API request. #  TODO: handle error
        """

        self.Handler.url = f"{creds.TATUM_BASE_URL}bitcoin/transaction/address/{address}"
        query_param = {
            "pageSize": page_size,
            "offset": offset,
            "txnType": txn_type.value,
            "blockFrom": block_from,
            "blockTo": block_to,
        }
        response = self.Handler.get(params=query_param)
        return response.json()

    def batch_get_transactions(self, addresses: list[str], txn_type: str = TransactionType.INCOMING.value) -> Mapping[str, Any]:
        """Retrieves transactions for multiple Bitcoin addresses in a single request.

        Args:
            addresses (list[str]): List of Bitcoin addresses to query.
            txn_type (str, optional): Type of transactions to filter (incoming or outgoing).
                Defaults to TransactionType.INCOMING.value.

        Returns:
            Mapping: Dictionary response containing a dictionary where keys are addresses and values are their transactions.
        """
        self.Handler.url = f"{creds.TATUM_BASE_URL}bitcoin/transaction/address/batch"

        payload = {"addresses": addresses, "txType": txn_type}

        response = self.Handler.post(data=payload)
        return response.json()

    def send_to_btc_address(
        self,
        *,
        from_address: str,
        to_address: str,
        value: int | float,
        sender_private_key: str,
        fee: str = None,
        change_address: str = None,
    ) -> Mapping[str, Any]:
        """Send Bitcoin to a specified address.

        This method sends Bitcoin from one address to another using the Tatum API. It constructs
        a payload with the necessary transaction information and posts it to the Tatum API endpoint
        for Bitcoin transactions.

        Args:
            from_address: The Bitcoin address from which funds are being sent.
            to_address: The Bitcoin address to which funds are being sent.
            value: The amount of Bitcoin to send.
            sender_private_key: The private key of the sender's address for signing the transaction.
            fee: The fee for the transaction in satoshis. Optional; if not provided, the Tatum API will calculate it.
            change_address: The address where the change from the transaction will be sent. Optional;
                if not provided, the change will be sent back to the from_address.

        Returns:
            A mapping object containing the response from the Tatum API, typically including transaction details.

        Raises:
            Exceptions related to network connectivity issues or API errors. #  TODO: handle exceptions gracefully
        """

        self.Handler.url = f"{creds.TATUM_BASE_URL}bitcoin/transaction"

        payload = {
            "fromAddress": [{"address": from_address, "privateKey": sender_private_key}],
            "to": [{"address": to_address, "value": value}],
            "fee": fee,
            "changeAddress": change_address,
        }
        response = self.Handler.post(data=payload)
        return response.json()

    def get_transaction_by_hash(self, txn_hash: str) -> Mapping[str, Any]:
        """Retrieve a Bitcoin transaction by its hash.

        Args:
            txn_hash: The hash of the transaction to retrieve.

        Returns:
            A mapping object containing the transaction details as returned by the Tatum API.

        Raises:
            Exceptions related to network connectivity issues or API errors.
        """
        self.Handler.url = f"{creds.TATUM_BASE_URL}bitcoin/transaction/{txn_hash}"
        response = self.Handler.get()
        return response.json()

    def get_unspent_transaction_output(self, txn_hash: str, index: int) -> Mapping[str, Any]:
        """Get details of an unspent transaction output (UTXO) for a given transaction hash and output index.

        Args:
            txn_hash: The hash of the transaction.
            index: The output index of the UTXO in the transaction.

        Returns:
            A mapping object containing details of the UTXO as returned by the Tatum API.

        Raises:
            Exceptions related to network connectivity issues or API errors.
        """
        self.Handler.url = f"{creds.TATUM_BASE_URL}bitcoin/utxo/{txn_hash}/{index}"
        response = self.Handler.get()
        return response.json()

    def get_transaction_mempool(self) -> Mapping[str, Any]:
        """Retrieve transactions currently in the Bitcoin mempool.

        Returns:
            A mapping object containing information about the transactions in the mempool as returned by the Tatum API.

        Raises:
            Exceptions related to network connectivity issues or API errors.
        """
        self.Handler.url = f"{creds.TATUM_BASE_URL}bitcoin/mempool"
        response = self.Handler.get()
        return response.json()

    def broadcast_transaction(self, tx_data: str, signature_id: str = None, index: int = None) -> Mapping[str, Any]:
        """Broadcast a signed Bitcoin transaction to the network.

        Args:
            tx_data: The raw, signed transaction data.
            signature_id: An optional signature identifier if the transaction was signed with Tatum's virtual accounts feature.
            index: An optional index to specify a nonce for the transaction; used with virtual accounts.

        Returns:
            A mapping object containing the response from the Tatum API, usually including the transaction's hash.

        Raises:
            Exceptions related to network connectivity issues, API errors, or invalid transaction data.  #   TODO: handle exceptions gracefully
        """
        self.Handler.url = f"{creds.TATUM_BASE_URL}bitcoin/broadcast"

        payload = {"txData": tx_data, "signatureId": signature_id, "index": index}
        response = self.Handler.post(data=payload)
        return response.json()


if __name__ == "__main__":
    wallet = BitcoinWallet()
    print(wallet.broadcast_transaction("62BD544D1B9031EFC330A3E855CC3A0D51CA5131455C1AB3BCAC6D243F65460D"))
