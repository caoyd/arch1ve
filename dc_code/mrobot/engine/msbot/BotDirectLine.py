import json
import time
from tornado.httpclient import HTTPClient, HTTPRequest


class BotDirectLine(object):
    START_CONVERSATION_TPL = "https://directline.botframework.com/api/conversations"
    SEND_MSG_TPL = "https://directline.botframework.com/api/conversations/{}/messages"
    GET_MSG_TPL = "https://directline.botframework.com/api/conversations/{}/messages?watermark={}"

    DIRECT_LINE_SECRET = "e-6i8uh4X1g.cwA.vbo.WW6G1lo_gpgz2qAswJVwoflaHNYaufab8r_AqCRtedA"

    def __init__(self):
        self.headers = {
            "Authorization": "BotConnector {}".format(self.DIRECT_LINE_SECRET)
        }

        # Get conversion ID
        request = HTTPRequest(self.START_CONVERSATION_TPL, headers=self.headers, body=json.dumps({}), method="POST")
        response = HTTPClient().fetch(request)
        data = json.loads(response.body.decode("utf-8"))
        self.cid = data["conversationId"]

        self.watermark = 1

    def chat(self, message):
        # Send message
        headers = {
            "Content-Type": "application/json",
            "Authorization": "BotConnector {}".format(self.DIRECT_LINE_SECRET)
        }
        data = {
            "conversationId": self.cid,
            "text": message
        }
        print(data)
        request = HTTPRequest(self.SEND_MSG_TPL.format(self.cid), headers=headers, body=json.dumps(data), method="POST")
        response = HTTPClient().fetch(request)
        print(response.code)
        if response.code == 204:
            time.sleep(5)

            # Get Bot reply
            request = HTTPRequest(self.GET_MSG_TPL.format(self.cid, self.watermark), headers=self.headers, method="GET")
            response = HTTPClient().fetch(request)
            data = json.loads(response.body.decode("utf-8"))
            self.watermark += 2
            msg = data["messages"][0]
            return msg["text"]
