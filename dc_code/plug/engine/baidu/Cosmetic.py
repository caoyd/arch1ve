import json
from urllib.parse import urlencode, quote
from tornado.httpclient import HTTPRequest

from engine.common.Handlers import SpiderHandler


class Cosmetic(SpiderHandler):
    API_KEY = "a771d8570a5029dcf40790ae8788c892"
    URL = "http://apis.baidu.com/jidichong/cosmetic/cosmetic?name={name}&company={company}&npage={npage}"

    async def do_process_logic(self):
        headers = {
            "apikey": self.API_KEY
        }

        name_args = self.get_query_arguments("name")
        company_args = self.get_query_arguments("company")
        page_args = self.get_query_arguments("npage")

        params = dict()
        params["name"] = quote(name_args[0]) if len(name_args) else ""
        params["company"] = quote(company_args[0]) if len(company_args) else ""
        params["npage"] = page_args[0] if len(page_args) else 1

        request = HTTPRequest(self.URL.format(**params), method="GET", headers=headers)
        response = await self.browser.fetch(request)

        html = response.body.decode("utf-8")
        result = json.loads(html)
        if result["status"] == 1:
            data = result["result"]["data"]
            self.send_json_response(data)
        else:
            self.send_json_response(result["msg"], 0)

