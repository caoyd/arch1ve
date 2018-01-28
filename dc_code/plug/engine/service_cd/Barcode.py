"""
国内商品条码信息查询
url1: http://www.ancc.org.cn/Service/queryTools/Internal.aspx
url2: http://search.anccnet.com/searchResult2.aspx?keyword=6904724022468
"""
import lxml.html
from urllib.parse import quote
from tornado.httpclient import HTTPRequest
from engine.common.Handlers import SpiderHandler
from engine.common.Utils import fake_useragent


class Barcode(SpiderHandler):
    async def do_process_logic(self):
        url_template = "http://search.anccnet.com/searchResult2.aspx?keyword={0}"

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "search.anccnet.com",
            "Referer": "http://www.ancc.org.cn/Service/queryTools/Internal.aspx",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": fake_useragent()
        }

        barcode = quote(self.get_query_argument("code"),encoding="gb2312")
        request = HTTPRequest(url_template.format(barcode), method="GET", headers=headers)
        response = await self.browser.fetch(request)
        html = response.body.decode("gb2312")
        root = lxml.html.fromstring(html)
        info_dds = root.xpath('//dl[@class="p-info"]/dd')
        supplier_dds = root.xpath('//dl[@class="p-supplier"]/dd')

        if len(info_dds) and len(supplier_dds):
            # result_list = []
            info = {
                "barcode": info_dds[0].text_content().strip(),
                "name": info_dds[1].text_content().strip(),
                "specs": info_dds[2].text_content().strip(),
                "desc": info_dds[3].text_content().strip(),
                "brand": supplier_dds[0].text_content().strip(),
                "manufacturer": supplier_dds[1].text_content().strip(),
            }
            self.send_json_response([info])
        else:
            self.send_json_response(self.config["error"]["NO_RESULT_ERR"], 0)

