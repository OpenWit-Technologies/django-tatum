"""Create a withdrawal from Tatum Ledger account to the blockchain.

BTC, LTC, DOGE, BCH

When withdrawal from Tatum is executed, all deposits, which are not processed yet are used as an
input and change is moved to pool address 0 of wallet for defined account's xpub.
If there are no unspent deposits, only last pool address 0 UTXO is used.
If balance of wallet is not sufficient, it is impossible to perform withdrawal from this account -> funds
were transferred to another linked wallet within system or outside of Tatum visibility.

For the first time of withdrawal from wallet, there must be some deposit made and funds are obtained from that.
Since there is no withdrawal, there was no transfer to pool address 0 and thus it is not present in vIn.
Pool transfer is identified by missing data.address property in response.
When last not cancelled withdrawal is not completed and thus there is no tx id of output transaction given,
we cannot perform next withdrawal.

ETH

Withdrawal from Tatum can be processed only from 1 account.
In Ethereum Blockchain, each address is recognized as an account and only funds from that account can be sent in 1 transaction.

Example:
Account A has 0.5 ETH, Account B has 0.3 ETH.
Account A is linked to Tatum Account 1, Account B is linked to Tatum Account 2.

Tatum Account 1 has balance 0.7 Ethereum and Tatum Account 2 has 0.1 ETH. Withdrawal from Tatum Account 1 can be at most 0.5 ETH,
even though balance in Tatum Private Ledger is 0.7 ETH. Because of this Ethereum Blockchain limitation,
withdrawal request should always contain sourceAddress, from which withdrawal will be made.
To get available balances for Ethereum wallet accounts, use the hint endpoint.

XRP

XRP withdrawal can contain DestinationTag except of address, which is placed in attr parameter of withdrawal request.
SourceTag of the blockchain transaction should be withdrawal ID for autocomplete purposes of withdrawals.

XLM

XLM withdrawal can contain memo except of address, which is placed in attr parameter of withdrawal request.
XLM blockchain does not have possibility to enter source account information.
It is possible to create memo in format 'destination|source', which is supported way of memo in Tatum and also there is
information about the sender account in the blockchain.

When withdrawal is created, all other withdrawals with the same currency are pending,
unless the current one is marked as complete or cancelled.

Tatum ledger transaction is created for every withdrawal request with operation type WITHDRAWAL.
The value of the transaction is the withdrawal amount + blockchain fee, which should be paid.
In the situation, when there is withdrawal for ERC20, XLM, or XRP based custom assets,
the fee is not included in the transaction because it is paid in different assets than the withdrawal itself."""


from django_tatum.apps.tatum.tatum_client.virtual_accounts.base import BaseRequestHandler
from django_tatum.apps.tatum.utils.response_handlers import handle_response_object


class Withdrawal(BaseRequestHandler):
    def __init__(self):
        """Initialize TatumVirtualCurrency class."""
        self.setup_request_handler("ledger/virtualCurrency")
        super().__init__()

    def store_withdrawal(
        self,
        sender_account_id: str,
        address: str,
        amount: str,
        fee: str,
        attr: str = None,
        compliant: bool = None,
        multiple_amounts: list[str] = None,
        payment_id: str = None,
        sender_note: str = None,
    ):
        """Store a withdrawal request to the Tatum Ledger.

        Args:
            sender_account_id (str): Sender account ID.
            address (str): Address to send the withdrawal to.
            amount (str): Amount to withdraw.
            fee (str): Fee to pay for the withdrawal.
            attr (str, optional): Additional attributes to add to the withdrawal. Defaults to None.
            compliant (bool, optional): Whether the withdrawal is compliant. Defaults to None.
            multiple_amounts (list[str], optional): Multiple amounts to withdraw. Defaults to None.
            payment_id (str, optional): Payment ID. Defaults to None.
            sender_note (str, optional): Sender note. Defaults to None.

        Returns:
            [type]: [description]
        """
        payload: dict[str, str] = {
            "senderAccountId": sender_account_id,
            "address": address,
            "amount": amount,
            "fee": fee,
        }

        if attr:
            payload["attr"] = attr
        if compliant:
            payload["compliant"] = compliant
        if multiple_amounts:
            payload["multipleAmounts"] = multiple_amounts
        if payment_id:
            payload["paymentId"] = payment_id
        if sender_note:
            payload["senderNote"] = sender_note

        self.setup_request_handler("offchain/withdrawal")

        response = handle_response_object(self.Handler.post(data=payload))
        return response

    def get_withdrawals(
        self,
        page_size: int,
        currency: str = None,
        status: str = None,
        offset: int = None,
    ):
        """Get withdrawals from the Tatum Ledger.

        Args:
            page_size (int): Page size.
            currency (str, optional): Currency to get withdrawals for. Defaults to None.
            status (str, optional): Status to get withdrawals for. Defaults to None.
            offset (int, optional): Offset. Defaults to None.

        Returns:
            [type]: [description]
        """
        query: dict[str, str] = {
            "pageSize": page_size,
        }

        if currency:
            query["currency"] = currency
        if status:
            query["status"] = status
        if offset:
            query["offset"] = offset

        self.setup_request_handler("offchain/withdrawal")

        response = handle_response_object(self.Handler.get(params=query))
        return response

    def complete_withdrawal(
        self,
        withdrawal_id: str,
        transaction_id: str,
    ):
        """nvoke complete withdrawal as soon as blockchain transaction ID is available.
        All other withdrawals for the same currency will be pending unless the last one is processed and marked as completed.

        Args:
            withdrawal_id (str): ID of the withdrawal to complete.
            transaction_id (str): Blockchain transaction ID of created withdrawal

        Returns:
            [type]: [description]
        """
        payload: dict[str, str] = {
            "id": withdrawal_id,
            "txId": transaction_id,
        }

        self.setup_request_handler(f"offchain/withdrawal/{withdrawal_id}/{transaction_id}")

        response = handle_response_object(self.Handler.post(data=payload))
        return response

    def cancel_withdrawal(
        self,
        withdrawal_id: str,
        revert: bool = True,
    ):
        """This method is helpful if you need to cancel the withdrawal if the blockchain transaction fails or is not yet processed.
        This does not cancel already broadcast blockchain transaction, only Tatum internal withdrawal,
        and the ledger transaction, that was linked to this withdrawal.
        By default, the transaction fee is included in the reverted transaction.

        There are situations, like sending ERC20 on ETH, TRC token on TRON, XLM or XRP based assets,
        when the fee should not be reverted, because e.g. the fee is in calculated in Ethereum and transaction
        was in ERC20 currency. In this situation, only the transaction amount should be reverted, not the fee.

        Args:
            withdrawal_id (str): ID of the withdrawal to cancel.
            revert (bool, optional): Whether to revert the transaction. Defaults to True.

        Returns:
            [type]: [description]
        """
        payload: dict[str, str] = {
            "id": withdrawal_id,
            "revert": revert,
        }

        self.setup_request_handler(f"offchain/withdrawal/{withdrawal_id}")

        response = handle_response_object(self.Handler.post(data=payload))
        return response

    def broadcast_signed_transactions(
        self,
        currency: str,
        transaction_data: str,
        withdrawal_id: str = None,
        signature_id: str = None,
    ):
        """Broadcast signed raw transaction end complete withdrawal associated with it.
        When broadcast succeeded but it is impossible to complete withdrawal,
        transaction id of transaction is returned and withdrawal must be completed manually.

        Args:
            currency (str) - 40 characters: Currency to broadcast the transaction for.
            transaction_data (str) - 500000 characters: Transaction data to broadcast.
            withdrawal_id (str, optional) - 24 characters: ID of the withdrawal to broadcast. Defaults to None.
            signature_id (str, optional) uuid: Signature ID. Defaults to None.

        Returns:
            [type]: [description]
        """
        payload: dict[str, str] = {
            "currency": currency,
            "transactionData": transaction_data,
        }

        if withdrawal_id:
            payload["withdrawalId"] = withdrawal_id
        if signature_id:
            payload["signatureId"] = signature_id

        self.setup_request_handler("offchain/withdrawal/broadcast")

        response = handle_response_object(self.Handler.post(data=payload))
        return response
