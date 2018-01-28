"""
国内厂商查询
url: http://www.ancc.org.cn/Service/queryTools/Internal.aspx
"""
import lxml.html
from urllib.parse import urlencode
from tornado.httpclient import HTTPRequest, AsyncHTTPClient

from engine.common.Handlers import SpiderHandler


class Manufacturer(SpiderHandler):
    async def do_process_logic(self):
        url = "http://www.ancc.org.cn/Service/queryTools/Internal.aspx"

        data = {
            '__VIEWSTATE': '/wEPDwULLTE5NTYxNDQyMTkPZBYCAgEPZBYCAhMPFgIeB1Zpc2libGVnFgYCAQ8PFgIeBFRleHQFBuWbm+W3nWRkAgMPDxYEHwFlHwBoZGQCBQ9kFgICAw8PFgQeC1JlY29yZGNvdW50AugHHhBDdXJyZW50UGFnZUluZGV4AgJkZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WBQUSUmFkaW9JdGVtT3duZXJzaGlwBQ1SYWRpb0l0ZW1JbmZvBQZSYWRpbzEFBlJhZGlvMgUGUmFkaW8zEaZPpzN0Hyxtl6UZaYNYC9zv4zo=',
            '__EVENTVALIDATION': '/wEWCgKc6NjoCgLLnru/BwKB7J3yDAKbg6TuCQLj+szOBgLC79P5DgLC78f5DgLC78v5DgLChPy+DQLjwOP9CN+1MsvstbN5QRzGNiwqoWHhybV9',
            'query-condition': 'RadioItemOwnership',
            'query-supplier-condition': 'Radio2',
            'btn_query': '查询'
        }

        name = self.get_query_argument("name")
        data["txtcode"] = name

        request = HTTPRequest(url, method="POST", body=urlencode(data))
        browser = AsyncHTTPClient()
        # response = await self.browser.fetch(request)
        response = await browser.fetch(request)
        html = response.body.decode("utf-8")

        root = lxml.html.fromstring(html)
        trs = root.xpath('//div[@class="section-body"]/table/tbody/tr')

        result_list = []
        for tr in trs:
            tds = tr.xpath('.//td')
            tmp = {
                "code": tds[0].text_content().strip(),
                "name": tds[1].text_content().strip(),
                "state": tds[2].text_content().strip(),
            }
            result_list.append(tmp)

        self.send_json_response(result_list)
