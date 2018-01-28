"""
成都出租车失物招领
url: http://www.cdtaxi.cn/shiwudj
"""
import lxml.html
from tornado.httpclient import HTTPRequest

from engine.common.Handlers import SpiderHandler
from engine.common.Utils import fake_useragent


class TaxiFound(SpiderHandler):
    async def do_process_logic(self):
        url = "http://www.cdtaxi.cn/zhaolingxx/index_{}.html"
        base_url = "http://www.cdtaxi.cn{}"

        headers = {
            "Host": "www.cdtaxi.cn",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "Origin": "http://www.cdtaxi.cn",
            # "Referer": "http://www.cdtaxi.cn/shiwudj/add.html",
            "User-Agent": fake_useragent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Upgrade-Insecure-Request": "1",
            "Accept-Language": "zh-CN,zh;q=0.8",
        }
        page_args = self.get_query_arguments("page")
        page = page_args[0] if len(page_args) else 1

        request = HTTPRequest(url.format(page), method="GET", headers=headers)
        response = await self.browser.fetch(request)

        html = response.body.decode("utf-8")
        root = lxml.html.fromstring(html)
        divs = root.xpath('//div[@class="special_p"]')
        result_list = []
        for div in divs:
            link = div.xpath('./a[1]')
            tmp_url = base_url.format(link[0].attrib["href"])
            request = HTTPRequest(tmp_url, method="GET", headers=headers)
            response = await self.browser.fetch(request)
            if response.code == 200:
                html = response.body.decode("utf-8")
                root = lxml.html.fromstring(html)
                found = root.xpath('//div[@class="newsshow"]/p')
                content = found[0].text_content().strip()

                # Content not in <p> but in <div>
                if not content:
                    found = root.xpath('//div[@class="newsshow"]/div')
                    content = found[1].text_content().strip()

                tmp = {
                    "content": content
                }
                result_list.append(tmp)
            else:
                continue
        self.send_json_response(result_list)

