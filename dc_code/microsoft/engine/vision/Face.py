import random

from tornado.escape import json_decode
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPError
from tornado.httpclient import HTTPRequest

from engine.common.Handlers import BaseHandler
from engine.common.Utils import resize_image


class Face(BaseHandler):

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

        url = self.config["urls"]["FACE_URL"]
        self.FACE_URL = "{0}/detect?returnFaceAttributes=age,gender,glasses".format(url)
        # self.FACE_URL = "{0}?returnFaceAttributes=age,gender,facialHair,glasses".format(url)
        self.KEYS = self.config["keys"]["FACE_KEYS"].split(',')
        self.LIMIT = int(self.config["global"]["IMAGE_SIZE_LIMIT"])
        self.FACE_HEADERS = {}

    def prepare(self):

        self.FACE_HEADERS = {
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

            request = HTTPRequest(self.FACE_URL, method="POST", headers=self.FACE_HEADERS, body=image_bytes)
            browser = AsyncHTTPClient()
            response = await browser.fetch(request)

            if response.code != 200:
                print("[ Face.py ]: to be written into log")
                self.send_json_response({"msg": "Invoke emotion API error"}, 0)
            else:
                result = json_decode(response.body)
                final_list = []
                for item in result:
                    glass = item["faceAttributes"]["glasses"]
                    if glass.upper() == "NOGLASSES":
                        with_glass = "no"
                    else:
                        with_glass = "yes"

                    template = {
                        "face_id": item["faceId"],
                        "age": item["faceAttributes"]["age"],
                        "gender": item["faceAttributes"]["gender"],
                        "glass": with_glass,
                    }
                    final_list.append(template)

                self.send_json_response(final_list)

        except KeyError:
            self.send_json_response({"msg": "Request Error"}, 0)

        except HTTPError:
            print("[ Emotion ]: (HTTPError) to be written into log")
            self.send_json_response({"msg": "Invoke face API error"}, 0)

