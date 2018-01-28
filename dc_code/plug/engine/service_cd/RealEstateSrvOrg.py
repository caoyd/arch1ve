"""
房地产服务机构查询
url: http://www.cdfgj.gov.cn/BusinessQuery/BusSearch.aspx?action=ucEnterpriseQuery&Class=13
"""
import re
import lxml.html
from urllib.parse import urlencode, unquote
from tornado.httpclient import HTTPRequest, HTTPError
from engine.common.Utils import fake_useragent

from engine.common.Handlers import SpiderHandler


class RealEstateCaptcha(SpiderHandler):
    async def do_process_logic(self):
        captcha_url = "http://www.cdfgj.gov.cn/BusinessQuery/UserControls/RandomCode.axd"
        headers = {
            "User-Agent": fake_useragent()
        }

        request = HTTPRequest(captcha_url, method="GET", headers=headers)
        response = await self.browser.fetch(request)

        # Get cookie from response header
        cookie = response.headers.get_list("Set-Cookie")[0]
        m = re.match('NETSCAPE_ID=(.*?);', cookie)
        if m:
            session = m.group(1)
        else:
            raise HTTPError(500, self.config["error"]["GET_COOKIE_ERR"])

        # Change cookie key name to JSESSIONID_INVOICE
        # The name of "JSESSIONID_INVOICE" must be fixed
        # The name of "JSESSIONID_INVOICE" must be fixed
        # The name of "JSESSIONID_INVOICE" must be fixed
        self.set_cookie("JSESSIONID_INVOICE", session)
        self.set_header("Content-Type", 'image')
        self.write(response.body)


class RealEstateHandler(SpiderHandler):
    async def do_process_logic(self):
        url = "http://www.cdfgj.gov.cn/BusinessQuery/BusSearch.aspx?action=ucEnterpriseQuery&Class=13"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": fake_useragent()
            # "Cookie": cookie,
            # "Cookie": self.request.headers["Cookie"],
        }

        tmp_cookie = self.get_query_argument("JSESSIONID_INVOICE")
        cookie = "NETSCAPE_ID=" + unquote(tmp_cookie)
        headers["Cookie"] = cookie

        org_type = self.get_query_argument("type")
        org_name = self.get_query_argument("name")
        captcha = self.get_query_argument("captcha")

        data = {
            "__VIEWSTATEGENERATOR": "74F44EA4",
            "ID_ucEnterpriseQuery$ddlEnterpriseType": org_type,
            "ID_ucEnterpriseQuery$txtName": org_name,
            "ID_ucEnterpriseQuery$txtRandomCode": captcha,
            "__VIEWSTATE": "/7q+lMJNWwtjfXt4wCcX/buarTl1CXpolPC5i21QOAmuD5888znPXyJ4SlAAfk0HmfeeVMx5H571JnvNXROoem0otSLiX73pzikEjaPaj46p9qqgfqNbyGfkbB/Z/JJYYy94w3IdjeW6j2lGVed6Xv8+uVMhNJtk7szqdCJoipUY6U/NttwCtUc88yYnLqU8eJ5YGFcEfDkdIyXfdZt4DerSIYjT+MqsOtRim09uZ1qyggVYvzatFmK/xNh3IjTHbHfO//R4fs99WseIBBDFL96lbWmXxbcSQ5rteHbUWwNv+OoNZ7hnOxXPuAQZC9gvjiUGpx00LavO9KfSfxLKpwm8LaKgENO9kP0l6zorHh2PvSgr8abhuJKcQuh46DoRihtKp1gYv/cbG+fUVwiLhGhOxsJoXlKJmk2Fyz+cXMy6SuDSFPMz/UWPSJIaSQodeP5L7+LNLIVH76uvww7oDAElcOjmjjmNB4riG52ZbS/yJkTWvFx5flwLZB/OJ7k17GkcFL93T8xuAfGaCUukdj3H+zkyNxI9z3E0BT2JZtBzIJlVpQZ9pnGndAa2hyo16aozmBUAnXN0La3DkArjB5SUcN21vuGR+tcts07tK+43j49imna17dWnC5NjfTU77DmtgNwchz111tFtyKLXrBX6RLNS6o4Sr7Adza9ysq8ANjSb5KBQem61ZA+i1lbOeORmfcoeTXqjIZ93r++lPEWdPaEv84lctfxLwwkHFstcgcqucxtG1Zi3zvglzoxZ7A+XgcmgDzBbEKkeGZg5kgsG5PePtCSk5I9FxEK/AirfO9WldVMSo2nm/IOUbMshpW5+e1p+3u3ApeQzGlUd3vaYXHUyll7/tKS1tlZnNN3ysQguUAJGCyZqqWEgXRpYmC2Wwf4bR7Shc997xP+QaOT31AfHOyiA0Bd5PYA70yvXsMISJdQZOpommTCszJeZJzqtOpspf5OhUyWObs/rCuKAUVcbZOZLCoGMoGJaUcMtH9p8W/K8qgu42K06ww6qrKfXvu2O9F6Zl8HNqsSjNupcmXRjx6My+gnj3YU1A/PrLyb/DPU+hTKQldreh0IH+bjU2a/E62ihTMdUSBE4mmGwLCa9/L0AKpD3LSaswdgc+c5ZbY+A7x342NI=",
            "ID_ucEnterpriseQuery$ImageButton4.x": 57,
            "ID_ucEnterpriseQuery$ImageButton4.y": 6,
        }

        request = HTTPRequest(url, method="POST", headers=headers, body=urlencode(data))
        response = await self.browser.fetch(request)
        html = response.body.decode("utf-8")
        root = lxml.html.fromstring(html)
        trs = root.xpath('//table[@id="ID_ucEnterpriseQuery_GridView1"]/tr')

        result_list = []
        for n in range(1, len(trs)):
            tds = trs[n].xpath('.//td')
            tmp = {
                "name": tds[0].text_content().strip(),
                "area": tds[1].text_content().strip(),
                "level": tds[2].text_content().strip(),
                "addr": tds[3].text_content().strip(),
            }
            result_list.append(tmp)

        self.send_json_response(result_list)


