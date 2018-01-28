import json
import random
import socket

from tornado.escape import json_decode
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPError
from tornado.httpclient import HTTPRequest

from engine.common.Utils import resize_image
from engine.common.Handlers import BaseHandler


class Match(BaseHandler):
    # Limit picture size to 4MB
    SIZE_LIMIT = 4000000

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

        self.MATCH = {}
        self.HEADERS = {}
        self.FACE_URL = self.config["urls"]["FACE_URL"]
        self.KEYS = self.config["keys"]["FACE_KEYS"].split(',')
        self.LIMIT = int(self.config["global"]["IMAGE_SIZE_LIMIT"])
        self.IS_LEGAL_REQUEST = False

    def prepare(self):
        http_header = self.request.headers

        if "Content-Type" in http_header:
            content_type = http_header["Content-Type"]
            if content_type.startswith("multipart/form-data"):
                self.IS_LEGAL_REQUEST = True

        self.HEADERS = {
            "Ocp-Apim-Subscription-Key": random.choice(self.KEYS),
        }

    async def post(self):
        try:
            if not self.IS_LEGAL_REQUEST:
                raise KeyError

            pic1_bytes = self.request.files["pic1"][0]["body"]
            pic2_bytes = self.request.files["pic2"][0]["body"]

            # Size of the uploaded picture is larger than 4MB
            pic1_bytes = resize_image(pic1_bytes) if len(pic1_bytes) > self.LIMIT else pic1_bytes
            pic2_bytes = resize_image(pic2_bytes) if len(pic2_bytes) > self.LIMIT else pic2_bytes

            # self.logger.info("pic1: {0} bytes, pic2: {1} bytes".format(len(pic1_bytes), len(pic2_bytes)))

            url = "{0}/detect".format(self.FACE_URL)
            self.HEADERS["Content-Type"] = "application/octet-stream"
            request1 = HTTPRequest(url, method="POST", headers=self.HEADERS, body=pic1_bytes)
            request2 = HTTPRequest(url, method="POST", headers=self.HEADERS, body=pic2_bytes)

            browser = AsyncHTTPClient()
            response1 = await browser.fetch(request1)
            response2 = await browser.fetch(request2)
            # Both responses' code are not 200
            # Raise HTTPError
            if not(response1.code == 200 and response2.code == 200):
                raise HTTPError

            # A dictionary list
            faces1 = json_decode(response1.body)
            faces2 = json_decode(response2.body)

            # Both pics are human vision
            if len(faces1) and len(faces2):
                self.MATCH["face1_detected"] = True
                self.MATCH["face2_detected"] = True

                face_id1 = json_decode(response1.body)[0]["faceId"]
                face_id2 = json_decode(response2.body)[0]["faceId"]

                url = "{0}/verify".format(self.FACE_URL)
                self.HEADERS["Content-Type"] = "application/json"
                payload = {
                    "faceId1": face_id1,
                    "faceId2": face_id2,
                }
                request = HTTPRequest(url, method="POST", headers=self.HEADERS, body=json.dumps(payload))
                browser = AsyncHTTPClient()
                response = await browser.fetch(request)

                if response.code == 200:
                    result = json_decode(response.body)
                    self.MATCH["same_person"] = result["isIdentical"]
                    self.MATCH["similarity"] = "{0:.2f}%".format(result["confidence"] * 100)
                    self.send_json_response(self.MATCH)
                else:
                    self.send_json_response({"msg": "API Backend Error"}, 0)

            else:  # Not all uploaded pics are human vision
                self.MATCH["face1_detected"] = True if len(faces1) else False
                self.MATCH["face2_detected"] = True if len(faces2) else False
                self.MATCH["same_person"] = False
                self.MATCH["similarity"] = "0.00%"
                self.send_json_response(self.MATCH)

        except KeyError:  # Upload error
            self.logger.error("caught KeyError in [ Match - post() ]")
            self.send_json_response({"msg": "Bad Request"}, 0)

        except HTTPError as err:
            self.logger.error(err)
            self.send_json_response({"msg": "api backend error"}, 0)

        except socket.gaierror as err:
            self.logger.error(err)
            self.send_json_response({"msg": "api backend error"}, 0)


