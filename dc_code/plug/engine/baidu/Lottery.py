import json
from tornado.httpclient import HTTPRequest
from engine.common.Handlers import SpiderHandler


class Lottery(SpiderHandler):
    API_KEY = "a771d8570a5029dcf40790ae8788c892"

    async def do_process_logic(self, *args):
        action = args[0]

        headers = {
            "apikey": self.API_KEY
        }

        if action == "query":
            url = "http://apis.baidu.com/apistore/lottery/lotteryquery?lotterycode={lottery}&recordcnt={record}"
            lottery = self.get_query_argument("lottery")
            record_args = self.get_query_arguments("record")

            params = {
                "lottery": lottery,
                "record": record_args[0] if len(record_args) else "1"
            }

            request = HTTPRequest(url.format(**params), method="GET", headers=headers)
            response = await self.browser.fetch(request)
            html = response.body.decode("utf-8")
            result = json.loads(html)
            if result["errNum"] == 0:
                self.send_json_response(result["retData"]["data"])
            else:
                self.send_json_response(self.config["error"]["SIMPLE_ERR"], 0)

        elif action == "list":
            url = "http://apis.baidu.com/apistore/lottery/lotterylist?lotterytype={type}"
            type_args = self.get_query_arguments("type")
            params = dict()
            params["type"] = type_args[0] if len(type_args) else "1"

            request = HTTPRequest(url.format(**params), method="GET", headers=headers)
            response = await self.browser.fetch(request)
            html = response.body.decode("utf-8")
            result = json.loads(html)

            data = result["retData"]
            self.send_json_response(data)

