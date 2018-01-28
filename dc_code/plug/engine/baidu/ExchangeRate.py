import json
from tornado.httpclient import HTTPRequest

from engine.common.Handlers import SpiderHandler


class ExchangeRate(SpiderHandler):
    API_KEY = "a771d8570a5029dcf40790ae8788c892"

    async def do_process_logic(self, *args):
        action = args[0]

        headers = {
            "apikey": self.API_KEY
        }

        if action == "type":
            url = "http://apis.baidu.com/apistore/currencyservice/type"
            request = HTTPRequest(url, method="GET", headers=headers)
            response = await self.browser.fetch(request)
            html = response.body.decode("utf-8")
            result = json.loads(html)
            data = result["retData"]
            self.send_json_response(data)

        elif action == "convert":
            url = "http://apis.baidu.com/apistore/currencyservice/currency?fromCurrency={from}&toCurrency={to}&amount={amount}"

            from_currency = self.get_query_argument("from")
            to_currency = self.get_query_argument("to")

            amount_args = self.get_query_arguments("amount")

            params = dict()
            params["from"] = from_currency
            params["to"] = to_currency
            params["amount"] = amount_args[0] if len(amount_args) else "1"

            request = HTTPRequest(url.format(**params), method="GET", headers=headers)
            response = await self.browser.fetch(request)
            html = response.body.decode("utf-8")
            result = json.loads(html)
            data = result["retData"]
            if isinstance(data, dict):
                self.send_json_response([data])
            else:
                self.send_json_response(self.config["error"]["REQUEST_ERR"], 0)

