"""
成都公积金demo
"""
import re
import lxml.html
from urllib.parse import urlencode
from urllib.parse import unquote
from tornado.httpclient import HTTPRequest
from tornado.httpclient import HTTPError

from engine.common.Handlers import BaseHandler
from engine.common.Utils import fake_useragent

USER_AGENTS = [
    "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; MI NOTE LTE Build/KTU84P) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.4 TBS/025489 Mobile Safari/533.1 MicroMessenger/6.3.13.49_r4080b63.740 NetType/cmnet Language/zh_CN",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; MI NOTE LTE Build/KTU84P) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.4 TBS/025489 Mobile Safari/533.1 MicroMessenger/6.3.13.49_r4080b63.740 NetType/cmnet Language/zh_CN",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13D15 MicroMessenger/6.3.13 NetType/WIFI Language/zh_CN",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Shuame; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.9.1.1000 Chrome/39.0.2146.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
    "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13",
    "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0b; Windows 98)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8",
    "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)",
    "Opera/9.20 (Windows NT 6.0; U; en)",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Shuame; .NET4.0C; .NET4.0E; GWX:RED)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2716.0 Safari/537.36 OPR/39.0.2234.0 (Edition developer)Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2716.0 Safari/537.36 OPR/39.0.2234.0 (Edition developer)",
]


class CDFundCaptcha(BaseHandler):
    async def get(self):
        captcha_url = "http://www.cdzfgjj.gov.cn/api.php?op=checkcode&code_len=4&font_size=20&width=130&height=50"
        headers = {
            "User-Agent": fake_useragent()
        }

        try:
            request = HTTPRequest(captcha_url, method="GET", headers=headers)
            response = await self.browser.fetch(request)

            if response.code == 200:
                # Get cookie from response header
                cookie = response.headers.get_list("Set-Cookie")[0]
                print("in captcha handler", cookie)
                m = re.match('PHPSESSID=(.*?);\s', cookie)
                if m:
                    session = m.group(1)
                else:
                    self.logger.debug("get cookie error")
                    raise HTTPError

                # Change cookie key name to JSESSIONID_INVOICE
                self.set_header("Set-Cookie", cookie)
                self.set_header("Content-Type", 'image')
                self.write(response.body)

            else:
                self.logger.debug("none 200 response code")
                raise HTTPError

        except HTTPError:
            self.logger.error("[ InvoiceCaptchaHandler - get() ] caught HTTPError")
            self.send_json_response({"msg": "invoice captcha error"}, 0)

    def post(self):
        self.write("404")


class CDFundLogin(BaseHandler):
    COOKIE = ""

    async def prepare(self):
        login_url = "http://www.cdzfgjj.gov.cn/index.php?m=content&c=gjj&a=login"
        tmp_cookie = self.get_query_argument("PHPSESSID")
        self.COOKIE = "PHPSESSID=" + unquote(tmp_cookie)
        print("in cdfund handler", self.COOKIE)

        card = self.get_query_argument("card")
        password = self.get_query_argument("password")
        captcha = self.get_query_argument("captcha")

        data = {
            "cardNo": card,
            "password": password,
            "verifyCode": captcha,
        }

        headers = {
            "User-Agent": fake_useragent(),
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": self.COOKIE,
        }

        request = HTTPRequest(login_url, method="POST", headers=headers, body=urlencode(data))
        response = await self.browser.fetch(request)
        if response.code == 200:
            print("login success")
        else:
            self.logger.debug("none 200 response code")
            raise HTTPError

    async def get(self):
        account_url = "http://www.cdzfgjj.gov.cn/index.php?m=content&c=gjj&a=account"
        headers = {
            "User-Agent": fake_useragent()
        }
        try:
            print(self.COOKIE)
            headers["Cookie"] = self.COOKIE

            request = HTTPRequest(account_url, method="GET", headers=headers)
            response = await self.browser.fetch(request)
            if response.code == 200:
                html = response.body.decode("utf-8")
                root = lxml.html.fromstring(html)
                tables = root.xpath('//div[@class="w-main"]/table')
                result_list = []
                for table in tables:
                    tds = table.xpath('.//tr/td[@class="c"]')
                    tmp = {
                        "client_no": tds[0].text_content().strip(),
                        "client_name": tds[1].text_content().strip(),
                        "deposit_to_date": tds[2].text_content().strip(),
                        "deposit_base": tds[3].text_content().strip(),
                        "deposit_unit": tds[4].text_content().strip(),
                        "deposit_personal": tds[5].text_content().strip(),
                        "balance": tds[6].text_content().strip(),
                        "account_status": tds[6].text_content().strip(),
                    }
                    result_list.append(tmp)
                self.send_json_response({"results": result_list})

            else:
                self.logger.debug("none 200 response code")
                raise HTTPError

        except HTTPError:
            self.logger.error("[ InvoiceCheckHandler - get() ] caught HTTPError")
            self.send_json_response({"msg": "invoice check error"}, 0)
