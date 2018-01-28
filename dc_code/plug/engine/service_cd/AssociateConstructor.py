"""
二级建造师查询
url: http://jzsgl.coc.gov.cn/archisearch/cxejjzs/rylist.aspx?sjbm=510000&qymc=&xm=&zclb=00&zczy=全部&zczsbh=&zch=&zyzgzsbh=
"""
import json
from urllib.parse import urlencode
from tornado.httpclient import HTTPRequest

from engine.common.Handlers import SpiderHandler
from engine.common.Utils import fake_useragent


class AssociateConstructor(SpiderHandler):
    async def do_process_logic(self):
        url = "http://jzsgl.coc.gov.cn/archisearch/AjaxAction/DataServices.aspx"

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'jzsgl.coc.gov.cn',
            'Origin': 'http://jzsgl.coc.gov.cn',
            'Referer': 'http://jzsgl.coc.gov.cn/archisearch/cxejjzs/rylist.aspx?sjbm=510000&qymc=&xm=&zclb=00&zczy=%E5%85%A8%E9%83%A8&zczsbh=&zch=&zyzgzsbh=',
            'X-Referer': 'http://jzsgl.coc.gov.cn/archisearch/cxejjzs/rylist.aspx?sjbm=510000&qymc=&xm=&zclb=00&zczy=%E5%85%A8%E9%83%A8&zczsbh=&zch=&zyzgzsbh=',
            'X-Requested-With': 'XMLHttpRequest',
            "User-Agent": fake_useragent()
        }

        name_args = self.get_query_arguments("name")
        ent_args = self.get_query_arguments("ent")
        # 注册号(川251141528602)
        reg_no_args = self.get_query_arguments("reg_no")
        # 注册证书编号
        cer_no_args = self.get_query_arguments("cer_no")
        # 执业资格证书编号
        qua_no_args = self.get_query_arguments("qua_no")
        page_args = self.get_query_arguments("page")

        params = {
            "Xm": name_args[0] if len(name_args) else "",
            "Qymc": ent_args[0] if len(ent_args) else "",
            "Zcbh": reg_no_args[0] if len(reg_no_args) else "",
            "Zsbh": cer_no_args[0] if len(cer_no_args) else "",
            "Zgzsbh": qua_no_args[0] if len(qua_no_args) else "",
            "Sjbm": "510000",   # 省级编号(51000-四川省)
            "Zclb": "00",
            "PageNo": int(page_args[0]) if len(page_args) else 1,
        }

        data = {
            'action': '020103',
            'param': params
        }

        labels = {
            "00": "最新状态",
            "01": "初始注册",
            "02": "变更注册",
            "03": "延续注册",
            "04": "增项注册",
            "05": "重新注册",
            "06": "遗失补办",
            "07": "注销注册",
        }

        request = HTTPRequest(url, method="POST", headers=headers, body=urlencode(data))
        response = await self.browser.fetch(request)
        data = json.loads(response.body.decode("utf-8"))
        constructors = data["AppendData"]["Data"]

        result_list = []
        for constructor in constructors:
            prof = []
            valid = []
            for item in constructor["zyList"].split('^'):
                tmp = item.split('|')
                prof.append(tmp[0])
                valid.append(tmp[1])

            profession = ','.join(prof)
            validity = ','.join(valid)

            tmp = {
                "province": constructor["sjmc"],
                "enterprise": constructor["qymc"],
                "name": constructor["xm"],
                "register_no": constructor["zcbh"].strip(),
                "register_certificate_no": constructor["zsbh"].strip(),
                "qualification_certificate_no": constructor["zgzsbh"].strip(),
                "profession": profession,
                "validity": validity,
                "type": labels[constructor["zclb"]]
            }
            result_list.append(tmp)

        self.send_json_response(result_list)
