import json
import time
import hashlib
import xml.etree.ElementTree as ET
import tornado.web
from tornado.httpclient import HTTPRequest, HTTPClient
from tornado.web import MissingArgumentError

# from engine.msbot.BotDirectLine import BotDirectLine

RESP_TEXT_TPL = "<xml><ToUserName><![CDATA[{to_user}]]></ToUserName>" \
                "<FromUserName><![CDATA[{from_user}]]></FromUserName>" \
                "<CreateTime>{create_time}</CreateTime>" \
                "<MsgType><![CDATA[text]]></MsgType>" \
                "<Content><![CDATA[{content}]]></Content></xml>"


class Wechat(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

        # self.directline = BotDirectLine()

    def get_access_token(self):
        url_tpl = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
        app_id = "wx1607782c4be9a033"
        app_secret = "762c5f00fe5d153631c54e265a22c7b0"
        request = HTTPRequest(url_tpl.format(app_id, app_secret), method="GET")
        response = HTTPClient().fetch(request)
        token = json.loads(response.body.decode("utf-8"))
        return token["access_token"]

    def get(self):
        self.write("~ shake shake ~")

    def post(self):
        data = self.request.body
        root = ET.fromstring(data.decode("utf-8"))
        recv_msg = dict()
        for child in root:
            recv_msg[child.tag] = child.text

        quick_resp_msg = {
            "to_user": recv_msg["FromUserName"],
            "from_user": recv_msg["ToUserName"],
            "create_time": int(time.time()),
            "content": "[echo] {}".format(recv_msg["Content"])
        }
        self.write(RESP_TEXT_TPL.format(**quick_resp_msg))

        # token = self.get_access_token()
        # time.sleep(5)
        # customer_url = "https://api.weixin.qq.com/customservice/kfaccount/add?access_token={}".format(token)
        # msg = {
        #     "kf_account":
        # }
        # request = HTTPRequest()



# class WechatHandshake(tornado.web.RequestHandler):
#     def get(self):
#         try:
#             signature = self.get_query_argument("signature")
#             timestamp = self.get_query_argument("timestamp")
#             nonce = self.get_query_argument("nonce")
#             echostr = self.get_query_argument("echostr")
#
#             token = "WhatTheFuck"
#
#             tmp_list = [token, timestamp, nonce]
#             sorted_list = sorted(tmp_list)
#             data = "".join(sorted_list)
#
#             # Compute digest
#             hash_sha1 = hashlib.sha1(data.encode("utf-8"))
#             digest = hash_sha1.hexdigest()
#             print("digest: {}".format(digest))
#
#             if digest == signature:
#                 self.write(echostr)
#             else:
#                 self.write("~ shake shake ~")
#         except MissingArgumentError:
#             self.write("~ shake shake ~")
