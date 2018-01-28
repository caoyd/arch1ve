"""
成都房屋"预/现售项目"
url: http://www.cdfgj.gov.cn/SCXX/ShowNew.aspx
"""
import lxml.html
from tornado.httpclient import HTTPRequest

from engine.common.Handlers import SpiderHandler
from engine.common.Utils import fake_useragent


class PreForSale(SpiderHandler):
    async def do_process_logic(self):
        url_template = "http://www.cdfgj.gov.cn/SCXX/ShowNew.aspx?iname={name}&region={district}&page={page}&st={from_time}&et={to_time}"

        headers = {
            "User-Agent": fake_useragent()
        }

        name_args = self.get_query_arguments("name")
        district_args = self.get_query_arguments("district")
        from_args = self.get_query_arguments("from")
        to_args = self.get_query_arguments("to")
        page_args = self.get_query_arguments("page")

        params = dict()
        params["name"] = name_args[0] if len(name_args) else ""
        params["district"] = district_args[0] if len(district_args) else ""
        params["from_time"] = from_args[0] if len(from_args) else ""
        params["to_time"] = to_args[0] if len(to_args) else ""
        params["page"] = page_args[0] if len(page_args) else 1

        request = HTTPRequest(url_template.format(**params), method="GET", headers=headers)
        response = await self.browser.fetch(request)
        html = response.body.decode("utf-8")

        root = lxml.html.fromstring(html)
        trs = root.xpath('//table[@id="ID_ucShowNew_gridView"]/tr')
        tr_num = len(trs)

        result_list = []
        for n in range(1, tr_num):
            tds = trs[n].xpath('.//td')
            tmp = {
                "no": tds[0].text_content().strip(),
                "name": tds[1].text_content().strip(),
                "district": tds[2].text_content().strip(),
                "addr": tds[3].text_content().strip(),
                "use": tds[4].text_content().strip(),
                "developer": tds[5].text_content().strip(),
                "area": tds[6].text_content().strip(),
                "time": tds[7].text_content().strip(),
            }
            result_list.append(tmp)

        self.send_json_response(result_list)

