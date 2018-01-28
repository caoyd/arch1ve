"""
成都出租车失物招领
url: http://www.cdtaxi.cn/shiwudj
"""
import re
import lxml.html
from urllib.parse import urlencode, unquote
from tornado.httpclient import HTTPRequest, HTTPError

from engine.common.Handlers import SpiderHandler
from engine.common.Utils import fake_useragent


class LostFoundCaptcha(SpiderHandler):
    async def do_process_logic(self):
        url = "http://www.cdtaxi.cn/shiwudj/add.html"
        captcha_url = "http://www.cdtaxi.cn/admin.php?m=flogin&a=verify"

        headers = {
            "User-Agent": fake_useragent()
        }

        # Request captcha and cookie
        request = HTTPRequest(captcha_url, method="GET", headers=headers)
        response = await self.browser.fetch(request)

        captcha_data = response.body
        # Get cookie from response header
        cookie = response.headers.get_list("Set-Cookie")[0]
        m = re.match('PHPSESSID=(.*?);\s', cookie)
        if m:
            session = m.group(1)
            cookie = "PHPSESSID={}".format(session)
        else:
            raise HTTPError(500, self.config["error"]["GET_COOKIE_ERR"])

        # Get form hidden value
        headers["Cookie"] = cookie
        request0 = HTTPRequest(url, method="GET", headers=headers)
        response0 = await self.browser.fetch(request0)
        html = response0.body.decode("utf-8")
        root = lxml.html.fromstring(html)
        hidden = root.xpath('//input[@name="__hash__"]')
        form_hash = str(hidden[0].attrib["value"])

        # Final response
        # Change cookie key name to JSESSIONID_INVOICE
        self.set_cookie("JSESSIONID_INVOICE", session)
        self.set_cookie("HIDDEN_FORM_HASH", form_hash)
        # self.set_header("Set-Cookie", cookie)
        self.set_header("Content-Type", 'image')
        self.write(captcha_data)


class LostFound(SpiderHandler):
    async def do_process_logic(self):
        url = "http://www.cdtaxi.cn/shiwudj/add.html"

        headers = {
            "Host": "www.cdtaxi.cn",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "Origin": "http://www.cdtaxi.cn",
            "Referer": "http://www.cdtaxi.cn/shiwudj/add.html",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Upgrade-Insecure-Request": "1",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "User-Agent": fake_useragent()
        }

        # Prepare cookie
        username = self.get_query_argument("name")
        form_hash = self.get_query_argument("HIDDEN_FORM_HASH")
        captcha = self.get_query_argument("captcha")
        tmp_cookie = self.get_query_argument("JSESSIONID_INVOICE")

        cookie = "PHPSESSID=" + unquote(tmp_cookie)
        headers["Cookie"] = cookie

        # Prepare post data
        tel_args = self.get_query_arguments("tel")
        pickup_args = self.get_query_arguments("pickup")
        pickup_time_args = self.get_query_arguments("pickup_time")
        getoff_args = self.get_query_arguments("getoff")
        getoff_time_args = self.get_query_arguments("getoff_time")
        company_args = self.get_query_arguments("company")
        car_type_args = self.get_query_arguments("car_type")
        plate_no_args = self.get_query_arguments("plate_no")
        invoice_sum_args = self.get_query_arguments("invoice_sum")
        invoice_code_args = self.get_query_arguments("invoice_code")
        invoice_no_args = self.get_query_arguments("invoice_no")
        lost_item_args = self.get_query_arguments("lost_item")
        msg_args = self.get_query_arguments("msg")
        time_args = self.get_query_arguments("time")

        data = {
            "username": username,
            "telephone": tel_args[0] if len(tel_args) else "",
            "first_ads": pickup_args[0] if len(pickup_args) else "",
            "uptime": pickup_time_args[0] if len(pickup_time_args) else "",
            "last_ads": getoff_args[0] if len(getoff_args) else "",
            "downtime": getoff_time_args[0] if len(getoff_time_args) else "",
            "gongsi": company_args[0] if len(company_args) else "",
            "chexing": car_type_args[0] if len(car_type_args) else "",
            "fapiao": invoice_sum_args[0] if len(invoice_sum_args) else "",
            "chepai": plate_no_args[0] if len(plate_no_args) else "",
            "daima": invoice_code_args[0] if len(invoice_code_args) else "",
            "haoma": invoice_no_args[0] if len(invoice_no_args) else "",
            "title": lost_item_args[0] if len(lost_item_args) else "",
            "content": msg_args[0] if len(msg_args) else "",
            "time": time_args[0] if len(time_args) else "",
            "dengji": "1",
            "verify": captcha,
            "__hash__": form_hash,
            "Submit": "提 交"

        }

        request = HTTPRequest(url, method="POST", headers=headers, body=urlencode(data))
        response = await self.browser.fetch(request)
        html = response.body.decode("utf-8")
        root = lxml.html.fromstring(html)
        span = root.xpath('//span[@class="green"]')[0]
        msg = span.text_content().strip()
        if msg != "留言提交成功":
            self.send_json_response({"msg": msg}, 0)
        else:
            self.send_json_response({"msg": msg})


class LostFoundRecord(SpiderHandler):
    async def do_process_logic(self):
        url = "http://www.cdtaxi.cn/shiwudj/index_{}.html"

        headers = {
            "Host": "www.cdtaxi.cn",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "Origin": "http://www.cdtaxi.cn",
            # "Referer": "http://www.cdtaxi.cn/shiwudj/add.html",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Upgrade-Insecure-Request": "1",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "User-Agent": fake_useragent()
        }

        page_args = self.get_query_arguments("page")
        page = page_args[0] if len(page_args) else 1

        request = HTTPRequest(url.format(page), method="GET", headers=headers)
        response = await self.browser.fetch(request)
        html = response.body.decode("utf-8")
        root = lxml.html.fromstring(html)
        items = root.xpath('//div[@class="xlost_item"]')
        total = len(items)
        result_list = []
        for n in range(1, total):
            tmp = {}

            tds = items[n].xpath('.//table/tbody/tr[1]/td')
            tmp["date"] = tds[0].text_content().strip()
            tmp["lost_item"] = tds[1].xpath('.//a')[0].attrib["title"]
            tmp["pickup"] = tds[2].xpath('.//a')[0].attrib["title"]
            tmp["getoff"] = tds[3].xpath('.//a')[0].attrib["title"]
            tmp["contact"] = tds[4].text_content().strip()
            tmp["tel"] = tds[5].text_content().strip()
            tmp["status"] = tds[6].text_content().strip()

            tr2 = items[n].xpath('.//table/tbody/tr[2]')[0]
            tmp["resp"] = tr2.text_content().strip().split('：')[1]
            result_list.append(tmp)

        self.send_json_response(result_list)

