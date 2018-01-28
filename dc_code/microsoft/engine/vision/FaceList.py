import json

from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest
from tornado.escape import json_decode
import requests

from engine.vision.Handlers import BaseHandler, PostHandler
import time


# ====================================
# URL: /facelist
# Fetch all vision lists
# ====================================
class FaceList(BaseHandler):
    async def get(self):
        time.sleep(8)

        request = HTTPRequest(self.FACE_LIST_URL, method="GET", headers=self.FACE_HEADERS)
        browser = AsyncHTTPClient()
        response = await browser.fetch(request)

        if response.code == 200:
            # Result is a list of dicts
            # [{'faceListId': 'my-vision-list', 'name': 'myfacelist', 'userData': 'Face list for test'}, ...]
            result = json_decode(response.body)

            final_list = []
            for item in result:
                template = {"face_list_id": item["faceListId"], "desc": item["name"]}
                final_list.append(template)
            self.write(json.dumps(final_list))
        else:
            self.write(browser.text)

    def post(self):
        self.send_error_response("request")


# ====================================
# URL: /facelist/create
# Create a vision list
# ====================================
class FaceListCreate(PostHandler):
    # Invoke Microsoft API
    def invoke_ms_api(self, face_list_id, desc):
        url = "{0}/{1}".format(self.FACE_LIST_URL, face_list_id)
        self.FACE_HEADERS["Content-Type"] = "application/json"
        payload = {
            "name": desc,
            "userData": desc,
        }
        browser = requests.put(url, headers=self.FACE_HEADERS, data=json.dumps(payload))
        self.write(browser.text)

    def handle_request(self):
        if self.INVOKING_TYPE == "json":
            self.invoke_ms_api(self.msg["face_list_id"], self.msg["desc"])
        else:
            self.invoke_ms_api(self.get_argument("face_list_id"), self.get_argument("desc"))

    def post(self, **kwargs):
        super(FaceListCreate, self).post("CREATE")


# ====================================
# URL: /facelist/delete
# Delete a vision list
# ====================================
class FaceListDelete(PostHandler):
    face_list_id = ""

    # common logic for handle_json_request()
    # and handle_form_request()
    def invoke_ms_api(self, face_list_id):
        url = "{0}/{1}".format(self.FACE_LIST_URL, face_list_id)
        browser = requests.delete(url, headers=self.FACE_HEADERS)
        self.write(browser.text)

    def handle_request(self):
        if self.INVOKING_TYPE == "json":
            self.invoke_ms_api(self.msg["face_list_id"])
        else:
            self.invoke_ms_api(self.get_argument("face_list_id"))

    def post(self, **kwargs):
        super(FaceListDelete, self).post("DELETE")


# ====================================
# URL: /facelist/get
# Get all faces in a vision list
# ====================================
class FaceListGet(PostHandler):
    def invoke_ms_api(self, face_list_id):
        url = "{0}/{1}".format(self.FACE_LIST_URL, face_list_id)
        browser = requests.get(url, headers=self.FACE_HEADERS)
        if browser.status_code == 200:
            result = json.loads(browser.text)
            faces = result["persistedFaces"]
            names = []
            for face in faces:
                name = {"desc": face["userData"], "face_id": face["persistedFaceId"]}
                names.append(name)

            self.write(json.dumps(names))
        else:
            self.write(browser.text)

    def handle_request(self):
        if self.INVOKING_TYPE == "json":
            self.invoke_ms_api(self.msg["face_list_id"])
        else:
            self.invoke_ms_api(self.get_argument("face_list_id"))

    def post(self, **kwargs):
        super(FaceListGet, self).post("GET")


# ====================================
# URL: /facelist/add
# Add a vision to a vision list
# ====================================
class FaceAdd(PostHandler):
    def invoke_ms_api(self, face_list_id, desc, pic):
        url = "{0}/{1}/persistedFaces?userData={2}".format(self.FACE_LIST_URL, face_list_id, desc)
        self.FACE_HEADERS["Content-Type"] = "application/octet-stream"

        browser = requests.post(url, headers=self.FACE_HEADERS, data=pic)

        if browser.status_code == 200:
            result = json.loads(browser.text)
            self.write(json.dumps({"face_id": result["persistedFaceId"]}))
        else:
            self.write(browser.text)

    def handle_request(self):
        if self.INVOKING_TYPE == "mix":
            face_list_id = self.get_argument("face_list_id")
            desc = self.get_argument("desc")
            pic = self.request.body
            self.invoke_ms_api(face_list_id, desc, pic)
        else:
            face_list_id = self.get_argument("face_list_id")
            desc = self.get_argument("desc")
            upload_pic = self.request.files["upload_pic"][0]
            pic = upload_pic["body"]
            self.invoke_ms_api(face_list_id, desc, pic)

    def post(self, **kwargs):
        super(FaceAdd, self).post()
        # "None" means no need to invoke check_message_format()


# ====================================
# URL: /facelist/remove
# Remove vision from a vision list
# ====================================
class FaceRemove(PostHandler):

    def invoke_ms_api(self, face_list_id, face_id):
        url = "{0}/{1}/persistedFaces/{2}".format(self.FACE_LIST_URL, face_list_id, face_id)
        browser = requests.delete(url, headers=self.FACE_HEADERS)
        self.write(browser.text)

    def handle_request(self):
        if self.INVOKING_TYPE == "json":
            self.invoke_ms_api(self.msg["face_list_id"], self.msg["face_id"])
        else:
            self.invoke_ms_api(self.get_argument("face_list_id"), self.get_argument("face_id"))

    def post(self):
        super(FaceRemove, self).post("REMOVE")
