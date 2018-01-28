# 贵阳社会动员服务平台首页
# URL: http://222.85.152.12:8803/JiaManage/guest/ShowJiaGuiYangHome.xhtml
import re
from urllib.parse import urlparse
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from tornado.httpclient import HTTPError
import lxml.html

from engine.common.Handlers import SpiderHandler
from engine.common.Utils import fake_useragent


async def get_detail(url):
    headers = {
        "User-Agent": fake_useragent()
    }
    request = HTTPRequest(url, method="GET", headers=headers)
    response = await AsyncHTTPClient().fetch(request)
    html = response.body.decode("utf-8")
    script = re.compile('<script>(.+?)</script>', re.DOTALL).findall(html)[0]

    matches = re.compile('start_num==(\d)\){(.+?)}', re.DOTALL).findall(script)
    details = {}
    for match in matches:
        pid = int(match[0])
        contents = re.compile('html\("(.+?)"\);').findall(match[1])

        detail = {
            "description": contents[0],
            "result": contents[1],
            "report_date": contents[2]
        }

        details[pid] = detail

    # Process NO. 6

    last_else_script = re.compile('else.?{(.+?)}', re.DOTALL).findall(script)[0]
    last_content = re.compile('html\("(.+?)"\);').findall(last_else_script)

    details[6] = {
        "description": last_content[0],
        "result": last_content[1],
        "report_date": last_content[2]
    }

    return details


class HelpPost(SpiderHandler):
    async def do_process_logic(self):
        url = "http://222.85.152.12:8803/JiaManage/guest/ShowJiaGuiYangHome.xhtml"
        purl = urlparse(url)
        base_url = purl.scheme + "://" + purl.netloc

        headers = {
            "User-Agent": fake_useragent()
        }

        request = HTTPRequest(url, method="GET", headers=headers)
        response = await self.browser.fetch(request)
        html = response.body.decode("utf-8")
        root = lxml.html.fromstring(html)
        trs = root.xpath('//div[@class="part_2_table float_left"]/table/tr')
        posts = {}
        detail_url = ""
        for tr in trs:
            a = tr.xpath('.//td[1]/a[1]')[0]
            title = a.text_content()
            finish_date = tr.xpath('.//td[2]')[0].text_content()

            detail_url = base_url + a.attrib["href"]
            post_id = int(detail_url.split("=")[1])

            post = {
                "title": title,
                "finish_date": finish_date
            }

            posts[post_id] = post

        real_url = detail_url.split('?')[0]
        details = await get_detail(real_url)

        for i in range(1, len(list(posts.keys()))+1):
            posts[i].update(details[i])

        results = []
        for k, v in posts.items():
            v["post_id"] = k
            results.append(v)

        # Invoke this method to send json response
        self.send_json_response(results)


class PraisePost(SpiderHandler):
    async def do_process_logic(self):
        url = "http://222.85.152.12:8803/JiaManage/guest/ShowJiaGuiYangHome.xhtml"
        purl = urlparse(url)
        base_url = purl.scheme + "://" + purl.netloc

        headers = {
            "User-Agent": fake_useragent()
        }

        request = HTTPRequest(url, method="GET", headers=headers)
        response = await self.browser.fetch(request)
        html = response.body.decode("utf-8")
        root = lxml.html.fromstring(html)
        trs = root.xpath('//div[@class="part_2_table float_right"]/table/tr')
        posts = {}
        detail_url = ""
        for tr in trs:
            a = tr.xpath('.//td[1]/a[1]')[0]
            title = a.text_content()
            finish_date = tr.xpath('.//td[2]')[0].text_content()

            detail_url = base_url + a.attrib["href"]
            post_id = int(detail_url.split("=")[1])

            post = {
                "title": title,
                "finish_date": finish_date
            }

            posts[post_id] = post

        real_url = detail_url.split('?')[0]
        details = await get_detail(real_url)

        for i in range(1, len(list(posts.keys()))+1):
            posts[i].update(details[i])

        results = []
        for k, v in posts.items():
            v["post_id"] = k
            results.append(v)

        # Invoke this method to send json response
        self.send_json_response(results)


class WeeklyReport(SpiderHandler):
    async def do_process_logic(self):
        url = "http://222.85.152.12:8803/JiaManage/guest/ShowJiaGuiYangHome.xhtml"

        headers = {
            "User-Agent": fake_useragent()
        }

        request = HTTPRequest(url, method="GET", headers=headers)
        response = await self.browser.fetch(request)
        html = response.body.decode("utf-8")
        root = lxml.html.fromstring(html)

        statistics = []

        # id="box1"
        div = root.xpath('//div[@id="box1"]')[0]
        script = div.xpath('.//script')[0].text_content()
        list_data = re.compile('value:(\d+).+?name:\'(.+?)\'').findall(script)
        box1 = {
            "id":1,
            "name": "共受理各类案件处理情况",
            "data": list_data
        }
        statistics.append(box1)

        # id="box2"
        div = root.xpath('//div[@id="box2"]')[0]
        script = div.xpath('.//script')[0].text_content()
        list_data = re.compile('data:.?\[(.+?)\]', re.DOTALL).findall(script)

        area = re.sub('[\t|\n|\r|\s|"]', '', list_data[0])
        area_list = area.split(',')

        data = re.sub('\s', '', list_data[1])
        data_list = [int(i) for i in data.split(',')]
        box2 = {
            "id": 2,
            "name": "各区（市、县）案件处理情况",
            "data": list(zip(area_list, data_list))
        }
        statistics.append(box2)

        # id="box3"
        div = root.xpath('//div[@id="box3"]')[0]
        script = div.xpath('.//script')[0].text_content()
        list_data = re.compile('data:.?\[(.+?)\]', re.DOTALL).findall(script)

        area = re.sub('[\t|\n|\r|\s|"]', '', list_data[0])
        area_list = area.split(',')

        data = re.sub('\s', '', list_data[1])
        data_list = [int(i) for i in data.split(',')]
        box3 = {
            "id": 3,
            "name": "市级联动部门案卷处理情况",
            "data": list(zip(area_list, data_list))
        }
        statistics.append(box3)

        # id="box4"
        div = root.xpath('//div[@id="box4"]')[0]
        script = div.xpath('.//script')[0].text_content()
        list_data = re.compile('data:.?\[(.+?)\]', re.DOTALL).findall(script)

        area = re.sub('[\t|\n|\r|\s|"]', '', list_data[0])
        area_list = area.split(',')

        data = re.sub('\s', '', list_data[1])
        data_list = [int(i) for i in data.split(',')]
        box4 = {
            "id": 4,
            "name": "平台案件类别",
            "data": list(zip(area_list, data_list))
        }
        statistics.append(box4)

        self.send_json_response(statistics)
