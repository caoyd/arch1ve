"""
食品生产许可证获证企业(SC,QS)
URL: http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=120&tableName=TABLE120&title=%CA%B3%C6%B7%C9%FA%B2%FA%D0%ED%BF%C9%BB%F1%D6%A4%C6%F3%D2%B5(SC)&bcId=145275419693611287728573704379
"""
import re
import lxml.html
from urllib.parse import quote, urlencode
from tornado.httpclient import HTTPRequest, HTTPClient

from engine.common.Handlers import SpiderHandler
from engine.common.Utils import fake_useragent


def fetch_cookie():
    response = HTTPClient().fetch("http://localhost:9527/api_cookie/fda")
    return response.body.decode("utf-8")


class FoodDrugAdmin(SpiderHandler):

    POST_DATA = {
        # 食品生产许可获证企业(SC)
        "sc": {
            "tableId": '120',
            "bcId": '145275419693611287728573704379',
            "tableName": 'TABLE120',
            "viewtitleName": 'COLUMN1591',
            "viewsubTitleName": 'COLUMN1597',
            "tableView": '%E9%A3%9F%E5%93%81%E7%94%9F%E4%BA%A7%E8%AE%B8%E5%8F%AF%E8%8E%B7%E8%AF%81%E4%BC%81%E4%B8%9A(SC)'
        },
        # 食品生产许可获证企业(QS)
        "qs": {
            "tableId": '91',
            "bcId": '137413698768984683499699272988',
            "tableName": 'TABLE91',
            "viewtitleName": 'COLUMN1156',
            "viewsubTitleName": 'COLUMN1157,COLUMN1155',
            "tableView": '%E9%A3%9F%E5%93%81%E7%94%9F%E4%BA%A7%E8%AE%B8%E5%8F%AF%E8%8E%B7%E8%AF%81%E4%BC%81%E4%B8%9A(QS)',
        },
        # 食品添加剂生产许可获证企业
        "addictive": {
            "tableId": '89',
            "bcId": '137403916083811026153735196207',
            "tableName": 'TABLE89',
            "viewtitleName": 'COLUMN1132',
            "viewsubTitleName": 'COLUMN1133,COLUMN1130',
            "tableView": '%E9%A3%9F%E5%93%81%E6%B7%BB%E5%8A%A0%E5%89%82%E7%94%9F%E4%BA%A7%E8%AE%B8%E5%8F%AF%E8%8E%B7%E8%AF%81%E4%BC%81%E4%B8%9A',
        },
        # 食品添加剂生产许可检验机构承检产品及相关标准
        "addictivecheck": {
            "tableId": '90',
            "bcId": '137395392579976004904078921814',
            "tableName": 'TABLE90',
            "viewtitleName": 'COLUMN1144',
            "viewsubTitleName": 'COLUMN1143',
            "tableView": '%E9%A3%9F%E5%93%81%E6%B7%BB%E5%8A%A0%E5%89%82%E7%94%9F%E4%BA%A7%E8%AE%B8%E5%8F%AF%E6%A3%80%E9%AA%8C%E6%9C%BA%E6%9E%84%E6%89%BF%E6%A3%80%E4%BA%A7%E5%93%81%E5%8F%8A%E7%9B%B8%E5%85%B3%E6%A0%87%E5%87%86',

        },
        # 国产保健食品
        "domestic": {
            "tableId": '30',
            "bcId": '118103385532690845640177699192',
            "tableName": 'TABLE30',
            "viewtitleName": 'COLUMN233',
            "viewsubTitleName": 'COLUMN235,COLUMN232',
            "tableView": '%E5%9B%BD%E4%BA%A7%E4%BF%9D%E5%81%A5%E9%A3%9F%E5%93%81',
        },
        # 进口保健食品
        "import": {
            "tableId": '31',
            "bcId": '118103387241329685908587941736',
            "tableName": 'TABLE31',
            "viewtitleName": 'COLUMN263',
            "viewsubTitleName": 'COLUMN262,COLUMN266',
            "tableView": '%E8%BF%9B%E5%8F%A3%E4%BF%9D%E5%81%A5%E9%A3%9F%E5%93%81',

        },
        # 进口化妆品
        "importcosmetic": {
            "tableId": '69',
            "bcId": '124053679279972677481528707165',
            "tableName": 'TABLE69',
            "viewtitleName": 'COLUMN801',
            "viewsubTitleName": 'COLUMN805,COLUMN811',
            "tableView": '%E8%BF%9B%E5%8F%A3%E5%8C%96%E5%A6%86%E5%93%81',

        },
        # 国产非特殊用途化妆品备案检验机构
        "inspectionorg": {
            "tableId": '83',
            "bcId": '131474662666676136335027594407',
            "tableName": 'TABLE83',
            "viewtitleName": 'COLUMN1003',
            # "viewsubTitleName": 'COLUMN805,COLUMN811',
            "tableView": '%E5%9B%BD%E4%BA%A7%E9%9D%9E%E7%89%B9%E6%AE%8A%E7%94%A8%E9%80%94%E5%8C%96%E5%A6%86%E5%93%81%E5%A4%87%E6%A1%88%E6%A3%80%E9%AA%8C%E6%9C%BA%E6%9E%84',

        },
        # 化妆品生产许可获证企业
        "productionent": {
            "tableId": '93',
            "bcId": '124053671285715992005675373538',
            "tableName": 'TABLE93',
            "viewtitleName": 'COLUMN1178',
            "viewsubTitleName": 'COLUMN1177,COLUMN1179',
            "tableView": '%E5%8C%96%E5%A6%86%E5%93%81%E7%94%9F%E4%BA%A7%E8%AE%B8%E5%8F%AF%E8%8E%B7%E8%AF%81%E4%BC%81%E4%B8%9A',
        },
        # 化妆品行政许可检验机构
        "admininspectionorg": {
            "tableId": '108',
            "bcId": '141403272796679344681283623477',
            "tableName": 'TABLE108',
            "viewtitleName": 'COLUMN1416',
            "viewsubTitleName": 'COLUMN1421',
            "tableView": '%E5%8C%96%E5%A6%86%E5%93%81%E8%A1%8C%E6%94%BF%E8%AE%B8%E5%8F%AF%E6%A3%80%E9%AA%8C%E6%9C%BA%E6%9E%84',
        },
        # 互联网药品信息服务
        "infosrv": {
            "tableId": '28',
            "bcId": '118715637133379308522963029631',
            "tableName": 'TABLE28',
            "viewtitleName": 'COLUMN212',
            "viewsubTitleName": 'COLUMN210',
            "tableView": '%E4%BA%92%E8%81%94%E7%BD%91%E8%8D%AF%E5%93%81%E4%BF%A1%E6%81%AF%E6%9C%8D%E5%8A%A1',
        },
        # 互联网药品交易服务
        "tradesrv": {
            "tableId": '33',
            "bcId": '118715801943244717582221630944',
            "tableName": 'TABLE33',
            "viewtitleName": 'COLUMN312',
            "viewsubTitleName": 'COLUMN310',
            "tableView": '%E4%BA%92%E8%81%94%E7%BD%91%E8%8D%AF%E5%93%81%E4%BA%A4%E6%98%93%E6%9C%8D%E5%8A%A1',
        },
        # 网上药店
        "onlinestore": {
            "tableId": '96',
            "bcId": '139468294509280829793942689586',
            "tableName": 'TABLE96',
            "viewtitleName": 'COLUMN1229',
            "viewsubTitleName": 'COLUMN1227',
            "tableView": '%E7%BD%91%E4%B8%8A%E8%8D%AF%E5%BA%97',

        },
        # 国家保健食品安全监督抽检（不合格产品）
        "unqualifiedhf": {
            "tableId": '112',
            "bcId": '143106780679359099093230607567',
            "tableName": 'TABLE112',
            "viewtitleName": 'COLUMN1453',
            "viewsubTitleName": 'COLUMN1457',
            "tableView": '%E5%9B%BD%E5%AE%B6%E4%BF%9D%E5%81%A5%E9%A3%9F%E5%93%81%E5%AE%89%E5%85%A8%E7%9B%91%E7%9D%A3%E6%8A%BD%E6%A3%80%EF%BC%88%E4%B8%8D%E5%90%88%E6%A0%BC%E4%BA%A7%E5%93%81%EF%BC%89',
        },
        # 国家保健食品安全监督抽检（合格产品）
        "qualifiedhf": {
            "tableId": '113',
            "bcId": '143106783126582192766779995431',
            "tableName": 'TABLE113',
            "viewtitleName": 'COLUMN1468',
            "viewsubTitleName": 'COLUMN1471',
            "tableView": '%E5%9B%BD%E5%AE%B6%E4%BF%9D%E5%81%A5%E9%A3%9F%E5%93%81%E5%AE%89%E5%85%A8%E7%9B%91%E7%9D%A3%E6%8A%BD%E6%A3%80%EF%BC%88%E5%90%88%E6%A0%BC%E4%BA%A7%E5%93%81%EF%BC%89',
        },
        # 国家食品安全监督抽检（不合格产品）
        "unqualifiedfood": {
            "tableId": '114',
            "bcId": '143106776907834761101199700381',
            "tableName": 'TABLE114',
            "viewtitleName": 'COLUMN1490',
            "viewsubTitleName": 'COLUMN1486',
            "tableView": '%E5%9B%BD%E5%AE%B6%E9%A3%9F%E5%93%81%E5%AE%89%E5%85%A8%E7%9B%91%E7%9D%A3%E6%8A%BD%E6%A3%80%EF%BC%88%E4%B8%8D%E5%90%88%E6%A0%BC%E4%BA%A7%E5%93%81%EF%BC%89',
        },
        # 国家食品安全监督抽检（合格产品）
        "qualifiedfood": {
            "tableId": '110',
            "bcId": '143106772371776780261602322547',
            "tableName": 'TABLE110',
            "viewtitleName": 'COLUMN1437',
            "viewsubTitleName": 'COLUMN1433',
            "tableView": '%E5%9B%BD%E5%AE%B6%E9%A3%9F%E5%93%81%E5%AE%89%E5%85%A8%E7%9B%91%E7%9D%A3%E6%8A%BD%E6%A3%80%EF%BC%88%E5%90%88%E6%A0%BC%E4%BA%A7%E5%93%81%EF%BC%89',
        }
    }

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

    async def do_process_logic(self, *args):
        category = args[0].lower()

        url_template = "http://app1.sfda.gov.cn/datasearch/face3/search.jsp"
        base_url_template = "http://app1.sfda.gov.cn/datasearch/face3/{}"

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "app1.sfda.gov.cn",
            "Origin": "http://app1.sfda.gov.cn",
            "User-Agent": fake_useragent(),
            "Referer": "http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=120&tableName=TABLE120&title=%CA%B3%C6%B7%C9%FA%B2%FA%D0%ED%BF%C9%BB%F1%D6%A4%C6%F3%D2%B5(SC)&bcId=145275419693611287728573704379",
            "Cookie": fetch_cookie()
        }

        query = self.get_query_argument("query")
        page_args = self.get_query_arguments("page")
        page = page_args[0] if len(page_args) else "1"

        # Assemble POST data
        if category not in self.POST_DATA:
            self.send_json_response(self.config["error"]["REQUEST_ERR"], 0)
            return
        else:
            data = self.POST_DATA[category]
            data["keyword"] = quote(query, encoding="utf-8")
            data["curstart"] = page

            request = HTTPRequest(url_template, method="POST", headers=headers, body=urlencode(data))
            response = await self.browser.fetch(request)

            html = response.body.decode("utf-8").strip()
            root = lxml.html.fromstring(html)
            links = root.xpath('//table/tr/td/p/a')
            result_list = []
            for link in links:
                href = link.attrib["href"].split(',')[1].strip("'")
                match = re.match(r'(content.+tableView=)(.+)(&Id.+)', href)
                href = "".join([match.group(1), quote(match.group(2), encoding="gb2312"), match.group(3)])
                tmp = {
                    "title": link.text_content().strip(),
                    "link": base_url_template.format(href)
                }
                result_list.append(tmp)

            self.send_json_response(result_list)
