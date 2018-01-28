"""
残疾证查询
url: http://www.cdpf.org.cn/2dzcx/
"""
import re
import lxml.html
from urllib.parse import urlencode, unquote
from tornado.httpclient import HTTPRequest, HTTPError

from engine.common.Handlers import SpiderHandler
from engine.common.Utils import fake_useragent


class DisabilityCertCaptcha(SpiderHandler):
    async def do_process_logic(self):
        captcha_url = "http://rkk.cdpf.org.cn/rand.jsp"
        headers = {
            "User-Agent": fake_useragent()
        }

        request = HTTPRequest(captcha_url, method="GET", headers=headers)
        response = await self.browser.fetch(request)

        # Get cookie from response header
        cookie = response.headers.get_list("Set-Cookie")[0]
        m = re.match('JSESSIONID=(.*?);\s', cookie)
        if m:
            session = m.group(1)
        else:
            raise HTTPError(500, self.config["error"]["GET_COOKIE_ERR"])

        # Change cookie key name to JSESSIONID_INVOICE
        self.set_cookie("JSESSIONID_INVOICE", session)
        # self.set_header("Set-Cookie", cookie)
        self.set_header("Content-Type", 'image')
        self.write(response.body)


class DisabilityCert(SpiderHandler):
    async def do_process_logic(self):
        url = "http://rkk.cdpf.org.cn/queryDistrictrecordCDPF.action"

        headers = {
            "User-Agent": fake_useragent(),
            "Content-Type": "application/x-www-form-urlencoded",
            # "Cookie": cookie,
            # "Cookie": self.request.headers["Cookie"],
        }

        tmp_cookie = self.get_query_argument("JSESSIONID_INVOICE")
        cookie = "JSESSIONID=" + unquote(tmp_cookie)
        headers["Cookie"] = cookie

        name = self.get_query_argument("name")
        no = self.get_query_argument("no")
        captcha = self.get_query_argument("captcha")

        data = {
            "getAjax": "true",
            "type": "211948D59141A611",
            "name": name,
            "cid": no,
            "cardType": 1,
            "checkCode": captcha
        }

        request = HTTPRequest(url, method="POST", headers=headers, body=urlencode(data))
        response = await self.browser.fetch(request)
        html = response.body.decode("gbk")
        root = lxml.html.fromstring(html)

        p1 = root.xpath('//p[@id="checkad1"]')
        p2 = root.xpath('//p[@id="checkad2"]')

        if len(p1):
            result = str(p1[0].text_content())
            self.send_json_response([{"msg": result}], 0)
        elif len(p2):
            result = str(p2[0].text_content())
            self.send_json_response([{"msg": result}])
        else:
            self.send_json_response(self.config["error"]["SIMPLE_ERR"], 0)





