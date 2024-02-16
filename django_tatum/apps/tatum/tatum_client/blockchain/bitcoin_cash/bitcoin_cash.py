from typing import Mapping, Any

from django_tatum.apps.tatum.tatum_client import creds
from django_tatum.apps.tatum.utils.requestHandler import RequestHandler


class BitcoinCashWallet:
    """
    A class for interacting with Bitcoin Cash (BCH) blockchain via the Tatum API.

    This class provides methods to generate a new BCH wallet, retrieve blockchain information,
    get block details by hash or height, create and broadcast transactions, and more, utilizing
    the Tatum API endpoints for Bitcoin Cash.

    Attributes:
        requestUrl (str): The base URL for the BCH wallet-related API requests.
        Handler (RequestHandler): An instance of RequestHandler configured with the API
                                  base URL and headers for making HTTP requests.

    Methods:
        generate_wallet: Generates a new BCH wallet including a private key, public key, and address.
        get_blockchain_info: Retrieves the current state of the BCH blockchain, including the latest block hash and height.
        get_block_hash: Retrieves the hash of a block at a given block height.
        get_block_by_hash: Retrieves details of a block by its hash or height.
        generate_transaction_by_hash: Fetches a transaction by its hash.
        get_deposit_address: Generates a deposit address from an xPub and index.
        generate_private_key: Generates a private key for a given mnemonic and index.
        send_to_bcash_address: Prepares and broadcasts a transaction to send BCH to an address.
        broadcast_transaction: Broadcasts a signed transaction to the BCH network.
    """

    def __init__(self) -> None:
        """
        Initializes the BitcoinCashWallet with the base URL for BCH wallet-related API requests
        and a RequestHandler for making the HTTP requests.
        """
        self.requestUrl = f"{creds.TATUM_BASE_URL}bcash/wallet"
        self.Handler = RequestHandler(
            self.requestUrl,
            {
                "Content-Type": "application/json",
                "x-api-key": creds.TATUM_API_KEY,
            },
        )

    def generate_wallet(self) -> Mapping[str, Any]:
        """
        Generates a new Bitcoin Cash wallet.

        Returns:
            A mapping object containing the wallet details such as address, private key, and mnemonic.
        """
        response = self.Handler.get()
        return response.json()

    def get_blockchain_info(self) -> Mapping[str, Any]:
        """
        Retrieves current blockchain information of the Bitcoin Cash network.

        Returns:
            A mapping object containing information about the current state of the BCH blockchain.
        """
        self.Handler.url = f"{creds.TATUM_BASE_URL}bcash/info"
        response = self.Handler.get()
        return response.json()

    def get_block_hash(self, block_no: str) -> Mapping[str, Any]:
        """
        Retrieves the hash of a specified block by its height.

        Args:
            block_no: The height of the block whose hash is to be retrieved.

        Returns:
            A mapping object containing the block hash.
        """
        self.Handler.url = f"{creds.TATUM_BASE_URL}bcash/block/hash/{block_no}"
        response = self.Handler.get()
        return response.json()

    def get_block_by_hash(self, hash_or_height: str) -> Mapping[str, Any]:
        """
        Retrieves details of a block by its hash or height.

        Args:
            hash_or_height: The hash or height of the block to retrieve.

        Returns:
            A mapping object containing details of the specified block.
        """
        self.Handler.url = f"{creds.TATUM_BASE_URL}bcash/block/{hash_or_height}"
        response = self.Handler.get()
        return response.json()

    def generate_transaction_by_hash(self, block_hash: str) -> Mapping[str, Any]:
        """
        Fetches a transaction by its hash.

        Args:
            block_hash: The hash of the transaction to retrieve.

        Returns:
            A mapping object containing the transaction details.
        """
        self.Handler.url = f"{creds.TATUM_BASE_URL}bcash/transaction/{block_hash}"
        response = self.Handler.get()
        return response.json()

    def get_deposit_address(self, xpub: str, index: int) -> Mapping[str, Any]:
        """
        Generates a deposit address from an xPub and index.

        Args:
            xpub: The extended public key to generate the address from.
            index: The index to generate the address for.

        Returns:
            A mapping object containing the deposit address.
        """
        self.Handler.url = f"{creds.TATUM_BASE_URL}bcash/address/{xpub}/{index}"
        response = self.Handler.get()
        return response.json()

    def generate_private_key(self, mnemonic: str, index: int = 0) -> Mapping[str, Any]:
        """
        Generates a private key for a given mnemonic and index.

        Args:
            mnemonic: The mnemonic seed phrase.
            index: The index to generate the private key for.

        Returns:
            A mapping object containing the private key.
        """
        self.Handler.url = f"{creds.TATUM_BASE_URL}bcash/wallet/priv"
        payload = {
            'index': index,
            'mnemonic': mnemonic
        }
        response = self.Handler.post(data=payload)
        return response.json()

    def send_to_bcash_address(
            self,
            *,
            tx_hash: str,
            index: int,
            to_address: str,
            value: int | float,
            sender_private_key: str,
            fee: str = None,
            change_address: str = None,
    ) -> Mapping[str, Any]:
        """
            Send Bitcoin Cash to a specified address by creating and broadcasting a transaction.

            This method creates a Bitcoin Cash transaction that sends a specified amount of BCH from
            one address to another. It leverages the Tatum API's "BchTransferBlockchain" operation to
            prepare and broadcast the transaction to the Bitcoin Cash network. The transaction is constructed
            using the provided UTXO details, recipient address, amount, and the sender's private key
            for signing. The fee and change address are optional; if not provided, default values are used.

            Args:
                tx_hash: The transaction hash of the UTXO to be spent.
                index: The index of the UTXO within its transaction.
                to_address: The recipient's Bitcoin Cash address.
                value: The amount of BCH to send, specified in satoshis (int) or as a float.
                sender_private_key: The private key of the sender, used to sign the transaction.
                fee: Optional; the fee for the transaction in satoshis. If not provided, a default fee is calculated.
                change_address: Optional; the address where the change from the transaction will be sent.
                                If not provided, change is returned to the sender's address.

            Returns:
                A dictionary containing the response from the Tatum API, typically including details like the
                transaction ID. The exact structure of this dictionary depends on the Tatum API's response.

            Raises:
                RequestsException: An error occurred during the HTTP request to the Tatum API.
        """
        self.Handler.url = f"{creds.TATUM_BASE_URL}bcash/transaction"

        payload = {
            "fromUTXO": [{"txHash": tx_hash, "index": index, "privateKey": sender_private_key}],
            "to": [{"address": to_address, "value": value}],
            "fee": fee,
            "changeAddress": change_address,
        }
        response = self.Handler.post(data=payload)
        return response.json()

    def broadcast_transaction(self, tx_data: str, signature_id: str = None, index: int = None) -> Mapping[str, Any]:
        """Broadcast a signed Bitcoin Cash transaction to the network.

        Args:
            tx_data: The raw, signed transaction data.
            signature_id: An optional signature identifier if the transaction was signed with Tatum's virtual accounts feature.
            index: An optional index to specify a nonce for the transaction; used with virtual accounts.

        Returns:
            A mapping object containing the response from the Tatum API, usually including the transaction's hash.

        Raises:
            Exceptions related to network connectivity issues, API errors, or invalid transaction data.  #   TODO: handle exceptions gracefully
        """
        self.Handler.url = f"{creds.TATUM_BASE_URL}bcash/broadcast"

        payload = {"txData": tx_data, "signatureId": signature_id, "index": index}
        response = self.Handler.post(data=payload)
        return response.json()


if __name__ == "__main__":
    wallet = BitcoinCashWallet()
    print(wallet.broadcast_transaction(tx_data='62BD544D1B9031EFC330A3E855CC3A0D51CA5131455C1AB3BCAC6D243F65460D'))
