import json
from tornado.httpclient import HTTPRequest
from tornado.httpclient import HTTPError
from tornado.web import MissingArgumentError

from engine.common.Handlers import SpiderHandler


class PhoneNo(SpiderHandler):
    API_KEY = "a771d8570a5029dcf40790ae8788c892"
    URL = "http://apis.baidu.com/chazhao/mobilesearch/phonesearch?phone={phone}"

    async def do_process_logic(self):
        headers = {
            "apikey": self.API_KEY
        }

        params = {
            "phone": self.get_query_argument("no")
        }

        request = HTTPRequest(self.URL.format(**params), method="GET", headers=headers)
        response = await self.browser.fetch(request)

        html = response.body.decode("utf-8")
        result = json.loads(html)

        if result["error"] == 0:
            data = result["data"]
            if isinstance(data, dict):
                data = [data]

            self.send_json_response(data)
        else:
            self.send_json_response(result["msg"], 0)


