"""

成都空气质量查询接口
aqi dict format
aqi = {
          "main_index": "130",
          "main_pollution": "首要污染物：PM2.5",
          "aqi_level": "轻度污染",
          "time": ""
          "pollutions": [
              {
                  "pollution": "XXXXXX",
                  "index": "3"
              },
              {
                  "pollution": "XXXXXX",
                  "index": "37"
              }
          ]
}
"""
import re
from tornado.httpclient import HTTPRequest
from tornado.httpclient import HTTPError
import lxml.html

from engine.common.Handlers import SpiderHandler
from engine.common.Utils import fake_useragent


class AirQuality(SpiderHandler):
    async def do_process_logic(self):
        # URL where source data(page) is located
        url = "http://www.cdepb.gov.cn/cdepbws/Web/gov/airquality.aspx"

        # Setup HTTP header for specific request
        headers = {
            "User-Agent": fake_useragent()
        }

        # Data passed with HTTP request if any
        # data = {}

        request = HTTPRequest(url, method="GET", headers=headers)
        response = await self.browser.fetch(request)
        html = response.body.decode("utf-8")
        root = lxml.html.fromstring(html)

        """
        BEGIN - Specific page analysis
        """
        city_aqi_div = root.xpath('//div[@class="CityAQI"]')[0]
        # city_aqi_div = root.xpath('/html/body/div[2]/div[5]/div[2]/div[2]')[0]
        main_index = city_aqi_div.xpath('.//span[@id="ContentBody_AqiData"]')[0].text_content()
        aqi_level = city_aqi_div.xpath('.//span[@id="ContentBody_StdName"]')[0].text_content()
        main_pollution = city_aqi_div.xpath('.//span[@id="ContentBody_FirstPoll"]')[0].text_content()
        update_time = city_aqi_div.xpath('.//span[@id="ContentBody_AQITime"]')[0].text_content()

        matches = re.findall('\d+', str(update_time))
        update_time = "{}-{}-{} {}".format(*matches)

        aqi = {
            "main_index": main_index,
            "main_pollution": main_pollution,
            "aqi_level": aqi_level,
            "time": update_time
        }

        pollution_table = city_aqi_div.xpath('//tbody')[0]
        pollution_table_tr = pollution_table.xpath('.//tr')

        pollutions = []
        for tr in pollution_table_tr:
            tds = tr.xpath('.//td')  # lxml
            poll = {
                # "pollution": tds[0].string,
                # "index": tds[1].string
                "pollution": tds[0].text_content(),
                "index": tds[1].text_content()
            }
            pollutions.append(poll)

        aqi["pollutions"] = pollutions
        """
        END - Specific page analysis
        """

        # Invoke this method to send json response
        self.send_json_response([aqi])

