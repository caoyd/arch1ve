"""
成都档案信息查询
url: http://i.rc114.com/InfoQuery_ArcInfo_Pub.aspx
"""
import re
import json
from tornado.httpclient import HTTPRequest
from engine.common.Utils import fake_useragent

from engine.common.Handlers import SpiderHandler


class FileInfo(SpiderHandler):
    async def do_process_logic(self):
        url = "http://i.rc114.com/InfoQuery_ArcInfo_Pub.aspx/queryData"

        headers = {
            "Content-Type": "application/json",
            "User-Agent": fake_useragent(),
        }

        data = {
            "name": self.get_query_argument("name"),
            "id": self.get_query_argument("id") ,
        }

        # browser = AsyncHTTPClient()
        request = HTTPRequest(url, method="POST", headers=headers, body=json.dumps(data))
        response = await self.browser.fetch(request)

        result = response.body.decode("utf-8")
        # data = json_decode(response.body)
        data = json.loads(result)
        tmp = data["d"]
        tmp = re.sub(r'\'', r'"', tmp)
        data = json.loads(tmp)

        # Receive JSON
        # {"state": 3 ,"error_message":'您的身份证位数不正确，请重新填写'}
        # {"state": 3 ,"error_message":'您的身份证无效，请重新填写'}

        if data["state"] == 3:
            self.send_json_response(data["error_message"], 0)

        # Receive JSON
        # {"error_message":'' ,"doc_state_title":'档案状态:' , "doc_id_title":'档案编号:',"doc_id": ...}
        else:
            # Found file info
            if "doc_id" in data:
                file_info = {
                    "name": data["person_name"],
                    "doc_id": data["doc_id"],
                    "school": data["graduate_school"],
                    "doc_state": data["doc_state"],
                    "doc_unit": data["doc_now_unit_name"],
                    "doc_old_unit": data["doc_old_unit"],
                    "doc_in_time": data["doc_in_time"]
                }
                self.send_json_response([file_info])
            # File info not found
            else:
                self.send_json_response(data["doc_state"], 0)

