import random

from tornado.escape import json_decode
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest
from tornado.httpclient import HTTPError

from engine.common.Handlers import BaseHandler
from engine.common.Utils import compute_score
from engine.common.Utils import resize_image


class Emotion(BaseHandler):

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

        self.EMOTION_URL = self.config["urls"]["EMOTION_URL"]
        self.KEYS = self.config["keys"]["EMOTION_KEYS"].split(',')
        self.LIMIT = int(self.config["global"]["IMAGE_SIZE_LIMIT"])
        self.EMOTION_HEADERS = {}

    def prepare(self):

        self.EMOTION_HEADERS = {
            "Ocp-Apim-Subscription-Key": random.choice(self.KEYS),
            "Content-Type": "application/octet-stream"
        }

    def get(self):
        pass

    async def post(self):
        try:
            # Client send image bytes as multipart/form-data
            # image_bytes = self.request.files["upload_pic"][0]["body"]

            # Client send image bytes through http body
            image_bytes = self.request.body
            if not image_bytes:
                raise KeyError

            # Check size of image
            image_bytes = resize_image(image_bytes) if len(image_bytes) > self.LIMIT else image_bytes

            request = HTTPRequest(self.EMOTION_URL, method="POST", headers=self.EMOTION_HEADERS, body=image_bytes)
            browser = AsyncHTTPClient()
            response = await browser.fetch(request)

            if response.code != 200:
                print("[ Emotion ]: to be written into log")
                self.send_json_response({"msg": "Invoke emotion API error"}, 0)
            else:
                # Result is a list of dicts
                result = json_decode(response.body)

                print(result)
                # Only choose first item
                if len(result):
                    scores = result[0]["scores"]
                    self.send_json_response(compute_score(scores))
                else:
                    self.send_json_response({"msg": "No face detected"})

        except KeyError:
            self.send_json_response({"msg": "Request Error"}, 0)

        except HTTPError:
            print("[ Emotion ]: (HTTPError) to be written into log")
            self.send_json_response({"msg": "Invoke emotion API error"}, 0)
