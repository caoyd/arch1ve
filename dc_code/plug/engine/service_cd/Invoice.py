"""
地税发票查询
url: http://182.151.197.163:7002/FPCY_SCDS_WW/
"""
import re
import lxml.html
from urllib.parse import urlencode, unquote
from tornado.httpclient import HTTPRequest, HTTPError
from engine.common.Utils import fake_useragent

from engine.common.Handlers import SpiderHandler


class InvoiceCaptcha(SpiderHandler):
    async def do_process_logic(self):
        captcha_url = "http://182.151.197.163:7002/FPCY_SCDS_WW/Captcha"
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


class InvoiceCheck(SpiderHandler):
    async def do_process_logic(self):
        url = "http://182.151.197.163:7002/FPCY_SCDS_WW/wwfpcy"

        headers = {
            "User-Agent": fake_useragent(),
            "Content-Type": "application/x-www-form-urlencoded",
            # "Cookie": cookie,
            # "Cookie": self.request.headers["Cookie"],
        }

        tmp_cookie = self.get_query_argument("JSESSIONID_INVOICE")
        cookie = "JSESSIONID=" + unquote(tmp_cookie)
        headers["Cookie"] = cookie

        invoice_code = self.get_query_argument("invoice_code")
        invoice_num = self.get_query_argument("invoice_num")
        invoice_psd = self.get_query_argument("invoice_psd")
        captcha = self.get_query_argument("captcha")

        data = {
            "fpdm0": invoice_code,
            "fphm0": invoice_num,
            "yzm0": invoice_psd,
            "imgcode": captcha,
        }

        request = HTTPRequest(url, method="POST", headers=headers, body=urlencode(data))
        response = await self.browser.fetch(request)
        html = response.body.decode("utf-8")
        root = lxml.html.fromstring(html)

        span1 = root.xpath('//span[@id="cxjj"]')
        span2 = root.xpath('//span[@id="message"]')

        if len(span1):
            result = str(span1[0].text_content())
            result = re.sub(r'\r|\n|\t', r'', result)
            self.send_json_response([{"msg": result}])
        elif len(span2):
            result = str(span2[0].text_content())
            result = re.sub(r'\r|\n|\t', r'', result)
            self.send_json_response([{"msg": result}])
        else:
            self.send_json_response(self.config["error"]["SIMPLE_ERR"], 0)





