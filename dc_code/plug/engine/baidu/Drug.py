from urllib.parse import urlencode, quote
from tornado.httpclient import HTTPRequest
from tornado.httpclient import HTTPError

from engine.common.Handlers import SpiderHandler


class Drug(SpiderHandler):
    API_KEY = "a771d8570a5029dcf40790ae8788c892"
    URL = "http://apis.baidu.com/tngou/drug/search?name={name}&keyword={keyword}&page={page}&rows={rows}&type={type}"

    async def get(self):
        headers = {
            "apikey": self.API_KEY
        }

        name = self.get_query_argument("name")
        keyword = self.get_query_argument("keyword")

        page_args = self.get_query_arguments("page")
        rows_args = self.get_query_arguments("rows")
        type_args = self.get_query_arguments("type")

        params = dict()
        params["name"] = quote(name)
        params["keyword"] = quote(keyword)
        params["page"] = page_args[0] if len(page_args) else 1
        params["rows"] = rows_args[0] if len(rows_args) else 20
        params["type"] = type_args[0] if len(type_args) else ""

        request = HTTPRequest(self.URL.format(**params), method="GET", headers=headers)
        response = await self.browser.fetch(request)
        if response.code == 200:
            html = response.body.decode("utf-8")
            print(html)
            # result = json.loads(html)
            # data = result["result"]["data"]
            # print(data)

        else:
            self.logger.debug("none 200 response code")
            raise HTTPError

