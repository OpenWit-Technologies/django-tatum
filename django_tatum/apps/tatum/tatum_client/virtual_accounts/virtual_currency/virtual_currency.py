"""
Register and use Tatum Private Ledger's virtual currencies.
You can create your own virtual currency and distribute it amongst your customers.
Virtual currencies are used to support FIAT currencies.
When a virtual currency is created with basePair of the FIAT currency, it is possible to perform transactions in
the private ledger in FIAT.
"""


from typing import Any
from django_tatum.apps.tatum.tatum_client.virtual_accounts.base import BaseRequestHandler
from django_tatum.apps.tatum.utils.response_handlers import handle_response_object
from django_tatum.apps.tatum.utils.utility import check_base_pair_currency_supported, validate_or_modify_currency_name


class TatumVirtualCurrency(BaseRequestHandler):
    def __init__(self):
        """Initialize TatumVirtualCurrency class."""
        self.setup_request_handler("ledger/virtualCurrency")
        super().__init__()

    def create_virtual_currency(
        self,
        name: str,
        supply: int,
        base_pair: str,
        description: str,
        account_code: str,
        account_number: str,
        accounting_currency: str,
        customer_external_id: str = None,
        customer_accounting_currency: str = None,
        base_rate: int = 1,
        customer_country: str = None,
        provider_country: str = None,
    ):
        """
        Create a virtual currency with given supply stored in account.
        This will create Tatum internal virtual currency.
        Every virtual currency must be prefixed with VC_.

        Every virtual currency must be pegged to existing FIAT or supported cryptocurrency.
        1 unit of virtual currency has then the same amount as 1 unit of the base currency it is pegged to.
        It is possible to set a custom base rate for the virtual currency.
        For example, if the baseRate = 2, then 1 virtual currency unit = 2 basePair units.

        This operation returns the newly created Tatum Ledger account with an initial balance set to the virtual currency's
        total supply. Total supply can be changed in the future.

        Note that a virtual currency is not a fungible token. To create a fungible token, deploy a token smart contract.

        Args:
            name (str): Name of the virtual currency. Must be prefixed with 'VC_'.
                If you fail to append `VC_` to the name, djano-tatum does it for you.
            supply (int): Supply of the virtual currency.
            base_pair (str): Base pair of the virtual currency. Transaction value will be calculated according to this base pair.
                e.g. 1 VC_VIRTUAL is equal to 1 BTC if base_pair is set to BTC.
            base_rate (int): Base rate of the virtual currency. Exchange rate of the base pair.
                Each unit of the created curency will represent value of baseRate*1 base_pair.

            description (str): Description of the virtual currency.
            account_code (str): Account code of the virtual currency. Can be used for bookkeeping to distinct account purpose.
            account_number (str): Account number from external system.
            accounting_currency (str): Accounting currency of the virtual currency.
            customer_external_id (str, optional): External id of the customer. Defaults to None.
            customer_accounting_currency (str, optional): Accounting currency of the customer. Defaults to None.
            customer_country (str, optional): Country of the customer. Defaults to None.
            provider_country (str, optional): Country of the provider. Defaults to None.

        Returns:
            [type]: [description]
        """
        if len(name) > 30:
            raise ValueError("name value cannot be more than 30 characters")
        if len(description) > 100:
            raise ValueError("description value cannot be more than 100 characters")
        if len(account_code) > 50:
            raise ValueError("account_code value cannot be more than 100 characters")
        if len(account_number) > 50:
            raise ValueError("account_number value cannot be more than 100 characters")
        if customer_external_id is not None and len(customer_external_id) > 99:
            raise ValueError("accounting_currency value cannot be more than 100 characters")
        if base_rate == 0 or base_rate < 0:
            raise ValueError("base_rate value cannot be 0 or less than 0")
        if supply == 0 or supply < 0:
            raise ValueError("supply value cannot be 0 or less than 0")
        base_pair_supported = check_base_pair_currency_supported(base_pair)
        if not base_pair_supported:
            raise ValueError(f"base pair value '{base_pair}' not supported.")

        currency_name: str = validate_or_modify_currency_name(name)

        payload: dict[str, Any] = {
            "name": currency_name,
            "supply": supply,
            "basePair": base_pair,
            "baseRate": base_rate,
            "description": description,
            "accountCode": account_code,
            "accountNumber": account_number,
            "accountingCurrency": accounting_currency,
        }

        if customer_external_id:
            payload["customerExternalId"] = customer_external_id
        if customer_accounting_currency:
            payload["customerAccountingCurrency"] = customer_accounting_currency
        if customer_country:
            payload["customerCountry"] = customer_country
        if provider_country:
            payload["providerCountry"] = provider_country

        self.setup_request_handler("ledger/virtualCurrency")

        response = handle_response_object(
            self.Handler.post(data=payload),
            additional_message="Virtual_currency created successfully.",
        )
        return response

    def update_virtual_currency(
        self,
        name: str = None,
        base_rate: int = 1,
        base_pair: str = None,
    ):
        currency_name: str = validate_or_modify_currency_name(name)

        if base_rate == 0 or base_rate < 0:
            raise ValueError("base_rate value cannot be 0 or less than 0")
        base_pair_supported = check_base_pair_currency_supported(base_pair)
        if not base_pair_supported:
            raise ValueError(f"base pair value '{base_pair}' not supported.")

        payload: dict[str, Any] = {
            "name": currency_name,
            "baseRate": base_rate,
            "basePair": base_pair,
        }

        self.setup_request_handler("ledger/virtualCurrency")

        response = handle_response_object(
            self.Handler.put(data=payload),
            additional_message="Virtual_currency updated successfully.",
        )
        return response

    def get_currency(
        self,
        currency_name: str,
    ):
        self.setup_request_handler(f"ledger/virtualCurrency/{currency_name}")
        response = handle_response_object(
            self.Handler.get(),
            additional_message="Virtual_currency retrieved successfully.",
        )
        return response

    def create_new_virtual_currency_supply(
        self,
        account_id: str,
        amount: str,
        payment_id: str = None,
        reference: str = None,
        transaction_code: str = None,
        recipient_note: str = None,
        counter_account: str = None,
        sender_note: str = None,
    ):
        """Create new supply of virtual currency linked on the given accountId.
        This method increases the total supply of the currency.

        This method creates Ledger transaction with operationType MINT with undefined counterAccountId.

        Args:
            account_id (str, required) max 24 characters: Ledger account with currency of the virtual currency,
            on which the operation will be performed.
            amount (str, required) max 38 characters: Amount of virtual currency to operate within this operation.
            payment_id (str, optional) max 100 characters: Identifier of the payment,
            shown for created Transaction within Tatum sender account.
            Defaults to None.
            reference (str, optional) max 100 characters: Reference of the payment.
            Defaults to None.
            transaction_code (str, optional) max 100 characters: For bookkeeping to distinct transaction purpose.
            Defaults to None.
            recipient_note (str, optional) max 500 characters: A note visible to both, sender and recipient.
            Available for both Mint and Revoke operations. Defaults to None.
            counter_account (str, optional) max 24 characters: External account identifier.
            By default, there is no counterAccount present in the transaction. Defaults to None.
            sender_note (str, optional) max 500 characters: Note visible to sender.
            Available in Revoke operation. Defaults to None.

        Returns:
            str: The internal reference to the transaction
            (a unique identifier of the transaction within the virtual account);
            if the transaction fails, use this reference to search through the logs.
        """
        self.setup_request_handler("ledger/virtualCurrency/mint")

        payload: dict[str, Any] = {
            "amount": amount,
            "accountId": account_id,
        }
        if payment_id:
            payload["paymentId"] = payment_id
        if reference:
            payload["reference"] = reference
        if transaction_code:
            payload["transactionCode"] = transaction_code
        if recipient_note:
            payload["recipientNote"] = recipient_note
        if counter_account:
            payload["counterAccount"] = counter_account
        if sender_note:
            payload["senderNote"] = sender_note

        response = handle_response_object(
            self.Handler.post(data=payload),
            additional_message=f"{amount} of virtual currency supply created successfully.",
        )
        return response

    def destroy_virtual_currency_supply(
        self,
        account_id: str,
        amount: str,
        payment_id: str = None,
        reference: str = None,
        transaction_code: str = None,
        recipient_note: str = None,
        counter_account: str = None,
        sender_note: str = None,
    ):
        """Destroy supply of virtual currency linked on the given accountId.
        This method decreases the total supply of the currency.

        This method creates Ledger transaction with operationType REVOKE with undefined counterAccountId.

        Args:
            account_id (str, required) max 24 characters: Ledger account with currency of the virtual currency,
            on which the operation will be performed.
            amount (str, required) max 38 characters: Amount of virtual currency to operate within this operation.
            payment_id (str, optional) max 100 characters: Identifier of the payment,
            shown for created Transaction within Tatum sender account.
            Defaults to None.
            reference (str, optional) max 100 characters: Reference of the payment. Defaults to None.
            transaction_code (str, optional) max 100 characters: For bookkeeping to distinct transaction purpose.
            Defaults to None.
            recipient_note (str, optional) max 500 characters: A note visible to both, sender and recipient.
            Available for both Mint and Revoke operations. Defaults to None.
            counter_account (str, optional) max 24 characters: External account identifier.
            By default, there is no counterAccount present in the transaction. Defaults to None.
            sender_note (str, optional) max 500 characters: Note visible to sender. Available in Revoke operation.
            Defaults to None.

        Returns:
            str: The internal reference to the transaction (a unique identifier of the transaction within the virtual account);
            if the transaction fails, use this reference to search through the logs.
        """
        self.setup_request_handler("ledger/virtualCurrency/revoke")

        payload: dict[str, Any] = {
            "amount": amount,
            "accountId": account_id,
        }
        if payment_id:
            payload["paymentId"] = payment_id
        if reference:
            payload["reference"] = reference
        if transaction_code:
            payload["transactionCode"] = transaction_code
        if recipient_note:
            payload["recipientNote"] = recipient_note
        if counter_account:
            payload["counterAccount"] = counter_account
        if sender_note:
            payload["senderNote"] = sender_note

        response = handle_response_object(
            self.Handler.post(data=payload),
            additional_message=f"{amount} of virtual currency supply destroyed successfully.",
        )
        return response


create_virtual_coin_payload: dict = {
    "name": "VC_krazo",
    "supply": "120,000,000,000,000,030,000",
    "base_pair": "GBP",
    "base_rate": 1,
    "description": "Money spent in the Ozark community",
    "account_code": "AcC-0300000001",
    "account_number": "3000000001",
    "accounting_currency": "GBP",
}


if __name__ == "__main__":
    tvc = TatumVirtualCurrency()
    tvc.create_virtual_currency(**create_virtual_coin_payload)
