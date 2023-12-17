"""These endpoints handle Order book operations like creating BID / ASK trades between Tatum Private
Virtual accounts, obtaining trade histories,
creating futures etc. It is possible to build an exchange based on the Ledger Accounts."""


from datetime import datetime
from django_tatum.apps.tatum.tatum_client.virtual_accounts.base import BaseRequestHandler
from django_tatum.apps.tatum.utils.response_handlers import handle_response_object


class OrderBook(BaseRequestHandler):
    def __init__(self):
        """Initialize TatumVirtualCurrency class."""
        self.setup_request_handler("trade")
        super().__init__()

    def create_instant_trade(
        self,
        type: str,
        price: str,
        amount: str,
        pair: str,
        currency_1_account_id: str,
        currency_2_account_id: str,
        fee_account_id: str,
        fee: int = None,
    ):
        """Create a trade between two virtual accounts.

        Args:
            type (str): Type of the regular trade, BUY, SELL. Acceptable types are the Enum: "BUY" "SELL".
            price (str): Price to buy / sell.
            amount (str): Amount of the trade to be bought / sold.
            pair (str): Pair to trade.
            currency_account_id (str): ID of the account of the currency 1 trade currency.
            currency2_account_id (str): ID of the account of the currency 2 trade currency.
            fee_account_id (str): ID of the account where fee will be paid, if any.
                If trade is a BUY or FUTURE_BUY type, feeAccountId must have same currency as a
                currency of currency2AccountId, and vice versa if trade is a SELL or FUTURE_SELL type,
                feeAccountId must have the same currency as a currency of currency1AccountId.
            fee (int, optional): Fee to pay for the trade. Defaults to None.

        Returns:
            [type]: [description]
        """

        payload: dict[str, str] = {
            "type": type,
            "price": price,
            "amount": amount,
            "pair": pair,
            "currency1AccountId": currency_1_account_id,
            "currency2AccountId": currency_2_account_id,
            "feeAccountId": fee_account_id,
        }

        if fee:
            payload["fee"] = fee

        self.setup_request_handler("trade")
        response = handle_response_object(self.Handler.post(data=payload))
        return response

    def create_future_trade(
        self,
        type: str,
        price: str,
        amount: str,
        pair: str,
        currency1_account_id: str,
        currency2_account_id: str,
        fee_account_id: str,
        percent_block: int,
        percent_penalty: int,
        seal_date: datetime,
        fee: int = None,
    ):
        """Create a future trade between two virtual accounts.

        Args:
            type (str): Type of the future trade, FUTURE_BUY, FUTURE_SELL.
            Acceptable types are the Enum: "FUTURE_BUY" "FUTURE_SELL"
            price (str) <= 38 characters: Price to buy / sell
            amount (str) <= 38 characters: Amount of the trade to be bought / sold.
            pair (str): Pair to trade.
            currency1_account_id (str): Currency1 account ID.
            currency2_account_id (str): Currency2 account ID.
            fee_account_id (str): ID of the account where fee will be paid, if any.
                If trade is a BUY or FUTURE_BUY type, feeAccountId must have same currency as a currency of currency2AccountId,
                and vice versa if trade is a SELL or FUTURE_SELL type, feeAccountId must have the same currency as a currency
                of currency1_account_id.
            percent_block (int): Percent block.
            percent_penalty (int): Percent penalty.
            seal_date (datetime): Seal date.
            fee (int, optional) <= 100: Percentage of the trade amount to be paid as a fee. Defaults to None.

        Returns:
            [type]: [description]
        """

        additional_attributes: dict[str, str] = {"sealDate": seal_date}
        if percent_block:
            additional_attributes["percentBlock"] = percent_block
        if percent_penalty:
            additional_attributes["percentPenalty"] = percent_penalty

        payload: dict[str, str] = {
            "type": type,
            "price": price,
            "amount": amount,
            "pair": pair,
            "currency1AccountId": currency1_account_id,
            "currency2AccountId": currency2_account_id,
            "feeAccountId": fee_account_id,
            "attr": additional_attributes,
        }

        if fee:
            payload["fee"] = fee

        self.setup_request_handler("trade")
        response = handle_response_object(self.Handler.post(data=payload))
        return response

    def obtain_chart_data_from_closed_trades(
        self,
        pair: str,
        start_time: int,
        end_time: int,
        time_frame: str,
        direction: str = "desc",
    ):
        """Obtain data from the closed trades for entering in a chart.
        Time interval is set between start_time and end_time and there is defined time frame.
        There can be obtained at most 200 time points in the time interval.

        Args:
            pair (str): Trading pair.
            start_time (int) >= 0: Start interval in UTC millis..
            end_time (int) >= 0: End interval in UTC millis.
            time_frame (str): Time frame of the chart.
                Enum: "MIN_1" "MIN_3" "MIN_5" "MIN_15" "MIN_30" "HOUR_1" "HOUR_4" "HOUR_12" "DAY" "WEEK" "MONTH" "YEAR"
            direction (str): Direction of sorting. Acceptable directions are "asc" and "desc". Defaults to "desc".

        Returns:
            [type]: [description]
        """

        payload: dict[str, str] = {
            "pair": pair,
            "from": start_time,
            "to": end_time,
            "timeFrame": time_frame,
            "direction": direction,
        }

        self.setup_request_handler("trade/chart")
        response = handle_response_object(self.Handler.post(data=payload))
        return response

    def list_all_historical_trades(
        self,
        page_size: int,
        count: bool,
        types: list[str],
        amount_operator: str,
        amount_value: str,
        fill_operator: str,
        fill_value: str,
        price_operator: str,
        price_value: str,
        created_operator: str,
        created_value: str,
        sort: list[str] = None,
        account_id: str = None,
        customer_id: str = None,
        offset: int = None,
        pair: str = None,
    ):
        """List all historical trades.

        Args:
            page_size (int) <= 50: Page size. Max number of items per page is 50.
            count (bool): Get the total trade pair count based on the filter. Either count or pageSize is accepted.
            types (list[str]): Trade types. Items Enum: "FUTURE_BUY" "FUTURE_SELL" "BUY" "SELL"
            amount_operator (str): Filtering operator to use to filter the amount of the trade.
                AND is used between the filter options.
                Defaults to None.
                accepted Enum values: "gte" "lte" "gt" "lt" "eq" "neq"
            amount_value (str): Amount value to be used in the amount filtering.
                Defaults to None.
            fill_operator (str): Fill operator to use to filter the fill of the trade.
                AND is used between the filter options.
                Defaults to None.
                accepted Enum values: "gte" "lte" "gt" "lt" "eq" "neq"
            fill_value (str): Fill value of the operation.
            price_operator (str): Price operator to use to filter the price of the trade.
                AND is used between the filter options.
                Defaults to None.
                accepted Enum values: "gte" "lte" "gt" "lt" "eq" "neq"
            price_value (str): Price value of the price filtering operation.
            created_operator (str): Created date to use to filter the trade.
                AND is used between the filter options.
                Defaults to None.
                Accepted Enum values: "gte" "lte" "gt" "lt" "eq" "neq"
            created_value (str): Created value.
            sort (list[str]): Sorts the result by selected property.
                The priority of the items is determined by order of the sort properties in array.
                Items Enum: "PRICE_ASC" "PRICE_DESC" "CREATED_ASC" "CREATED_DESC" "AMOUNT_ASC" "AMOUNT_DESC"
                    "FILL_ASC" "FILL_DESC" "FEE_ASC" "FEE_DESC"
                Defaults to None.
            account_id (str, optional): Account ID. If present, only closed trades for given account will be present.
                Defaults to None.
            customer_id (str, optional): Customer ID. If present, only closed trades for given customer will be present.
                Defaults to None.
            offset (int, optional): Offset to obtain next page of the data.
                Defaults to None.
            pair (str, optional) 3 <= pair <= 30 characters: Trade pair. If present, list historical trades for that pair.
                Defaults to None.

        Returns:
            [type]: [description]
        """

        payload: dict[str, str] = {
            "pageSize": page_size,
            "count": count,
            "types": types,
            "amount": {"op": amount_operator, "value": amount_value},
            "fill": {"op": fill_operator, "value": fill_value},
            "price": {"op": price_operator, "value": price_value},
            "created": {"op": created_operator, "value": created_value},
        }

        if sort:
            payload["sort"] = sort
        if account_id:
            payload["accountId"] = account_id
        if customer_id:
            payload["customerId"] = customer_id
        if offset:
            payload["offset"] = offset
        if pair:
            payload["pair"] = pair

        self.setup_request_handler("trade/history")
        response = handle_response_object(self.Handler.post(data=payload))
        return response

    def list_all_active_buy_trades(
        self,
        account_id: str,
        customer_id: str,
        page_size: int,
        amount_operator: str,
        amount_value: str,
        fill_operator: str,
        fill_value: str,
        price_operator: str,
        price_value: str,
        created_operator: str,
        created_value: str,
        sort: list[str] = None,
        offset: int = None,
        pair: str = None,
        count: bool = None,
        trade_type: str = None,
    ):
        """List all active buy trades.

        Args:
            account_id (str): Account ID. If present, list current active sell trades for that account.
            customer_id (str): Customer ID. If present, list current active buy trades for that customer.
            page_size (int) <= 50: Page size. Max number of items per page is 50.
            amount_operator (str): Filtering operator to use to filter the amount of the trade.
                AND is used between the filter options.
                Defaults to None.
                accepted Enum values: "gte" "lte" "gt" "lt" "eq" "neq"
            amount_value (str): Amount value to be used in the amount filtering.
                Defaults to None.
            fill_operator (str): Fill operator to use to filter the fill of the trade.
                AND is used between the filter options.
                Defaults to None.
                accepted Enum values: "gte" "lte" "gt" "lt" "eq" "neq"
            fill_value (str): Fill value of the operation.
            price_operator (str): Price operator to use to filter the price of the trade.
                AND is used between the filter options.
                Defaults to None.
                accepted Enum values: "gte" "lte" "gt" "lt" "eq" "neq"
            price_value (str): Price value of the price filtering operation.
            created_operator (str): Created date to use to filter the trade.
                AND is used between the filter options.
                Defaults to None.
                Accepted Enum values: "gte" "lte" "gt" "lt" "eq" "neq"
            created_value (str): Created value.
            sort (list[str]): Sorts the result by selected property.
                The priority of the items is determined by order of the sort properties in array.
                Items Enum: "PRICE_ASC" "PRICE_DESC" "CREATED_ASC" "CREATED_DESC" "AMOUNT_ASC" "AMOUNT_DESC"
                    "FILL_ASC" "FILL_DESC" "FEE_ASC" "FEE_DESC"
                Defaults to None.
            offset (int, optional): Offset to obtain next page of the data.
                Defaults to None.
            pair (str, optional) 3 <= pair <= 30 characters: Trade pair. If present, list historical trades for that pair.
                Defaults to None.
            count (bool, optional): Get the total trade pair count based on the filter. Either count or pageSize is accepted.
                Defaults to None.
            trade_type (str, optional): Trade type.
                Defaults to None.
                Accepted Enum Values: "FUTURE_SELL" "SELL".

            Returns:
            [type]: [description]
        """

        payload: dict[str, str] = {
            "accountId": account_id,
            "customerId": customer_id,
            "pageSize": page_size,
            "amount": {"op": amount_operator, "value": amount_value},
            "fill": {"op": fill_operator, "value": fill_value},
            "price": {"op": price_operator, "value": price_value},
            "created": {"op": created_operator, "value": created_value},
        }

        if sort:
            payload["sort"] = sort
        if offset:
            payload["offset"] = offset
        if pair:
            payload["pair"] = pair
        if count:
            payload["count"] = count
        if trade_type:
            payload["type"] = trade_type

        self.setup_request_handler("trade/buy")
        response = handle_response_object(self.Handler.post(data=payload))
        return response

    def list_all_active_sell_trades(
        self,
    ):
        pass

    def list_all_matched_future_sell_buy_trade_orders(
        self,
        account_id: str,
        customer_id: str,
        page_size: int,
        amount_operator: str,
        amount_value: str,
        fill_operator: str,
        fill_value: str,
        price_operator: str,
        price_value: str,
        created_operator: str,
        created_value: str,
        sort: list[str] = None,
        offset: int = None,
        pair: str = None,
        count: bool = None,
        trade_type: str = None,
    ):
        """List all matched future sell buy trades.

        Args:
            account_id (str): Account ID. If present, list current active sell trades for that account.
            customer_id (str): Customer ID. If present, list current active buy trades for that customer.
            page_size (int) <= 50: Page size. Max number of items per page is 50.
            amount_operator (str): Filtering operator to use to filter the amount of the trade.
                AND is used between the filter options.
                Defaults to None.
                accepted Enum values: "gte" "lte" "gt" "lt" "eq" "neq"
            amount_value (str): Amount value to be used in the amount filtering.
                Defaults to None.
            fill_operator (str): Fill operator to use to filter the fill of the trade.
                AND is used between the filter options.
                Defaults to None.
                accepted Enum values: "gte" "lte" "gt" "lt" "eq" "neq"
            fill_value (str): Fill value of the operation.
            price_operator (str): Price operator to use to filter the price of the trade.
                AND is used between the filter options.
                Defaults to None.
                accepted Enum values: "gte" "lte" "gt" "lt" "eq" "neq"
            price_value (str): Price value of the price filtering operation.
            created_operator (str): Created date to use to filter the trade.
                AND is used between the filter options.
                Defaults to None.
                Accepted Enum values: "gte" "lte" "gt" "lt" "eq" "neq"
            created_value (str): Created value.
            sort (list[str]): Sorts the result by selected property.
                The priority of the items is determined by order of the sort properties in array.
                Items Enum: "PRICE_ASC" "PRICE_DESC" "CREATED_ASC" "CREATED_DESC" "AMOUNT_ASC" "AMOUNT_DESC"
                    "FILL_ASC" "FILL_DESC" "FEE_ASC" "FEE_DESC"
                Defaults to None.
            offset (int, optional): Offset to obtain next page of the data.
                Defaults to None.
            pair (str, optional) 3 <= pair <= 30 characters: Trade pair. If present, list historical trades for that pair.
                Defaults to None.
            count (bool, optional): Get the total trade pair count based on the filter. Either count or pageSize is accepted.
                Defaults to None.
            trade_type (str, optional): Trade type.
                Defaults to None.
                Accepted Enum Values: "FUTURE_SELL" "SELL".

            Returns:
                [type]: [description]
        """

        payload: dict[str, str] = {
            "accountId": account_id,
            "customerId": customer_id,
            "pageSize": page_size,
            "amount": {"op": amount_operator, "value": amount_value},
            "fill": {"op": fill_operator, "value": fill_value},
            "price": {"op": price_operator, "value": price_value},
            "created": {"op": created_operator, "value": created_value},
        }

        if sort:
            payload["sort"] = sort
        if offset:
            payload["offset"] = offset
        if pair:
            payload["pair"] = pair
        if count:
            payload["count"] = count
        if trade_type:
            payload["type"] = trade_type

        self.setup_request_handler("trade/matched")
        response = handle_response_object(self.Handler.post(data=payload))
        return response

    def get_existing_trade(self, trade_id: str,):
        """Get existing trade.

        Args:
            trade_id (str): Trade ID.

        Returns:
            [type]: [description]
        """

        self.setup_request_handler(f"trade/{trade_id}")
        response = handle_response_object(self.Handler.get())
        return response

    def cancel_existing_trade(self, trade_id: str,):
        """Cancel existing trade.

        Args:
            trade_id (str): Trade ID.

        Returns:
            [type]: [description]
        """

        self.setup_request_handler(f"trade/{trade_id}")
        response = handle_response_object(self.Handler.delete())
        return response

    def cancel_all_existing_trades_for_account(self, account_id: str,):
        """Cancel all existing trades for account.

        Args:
            account_id (str): Account ID.

        Returns:
            [type]: [description]
        """

        self.setup_request_handler(f"trade/account/{account_id}")
        response = handle_response_object(self.Handler.delete())
        return response
