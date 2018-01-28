import json
import tornado.web
import tornado.gen
from tornado.escape import json_decode
from tornado.web import MissingArgumentError
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest
from json.decoder import JSONDecodeError


# ==================================================================
# Basic APIHandler
# * Rewrite prepare() method to determine CALL_TYPE(json,form,mix...)
# * Define check_json() method to check JSON format
# * Define send_error_response() to send different types of error
# ==================================================================
class BaseHandler(tornado.web.RequestHandler):
    INVOKING_TYPE = ""

    FACE_URL = "https://api.projectoxford.ai/vision/v1.0"
    FACE_LIST_URL = "https://api.projectoxford.ai/vision/v1.0/facelists"
    EMOTION_URL = "https://api.projectoxford.ai/emotion/v1.0/recognize"

    FACE_HEADERS = {
        # "Ocp-Apim-Subscription-Key": "8107ac9d6b1c4c508312f640d55fae21",  # 67784480@qq.com
        "Ocp-Apim-Subscription-Key": "f2eaddfacf0b4618b4c84fa2552549b2",  # ski2per@163.com
    }
    EMOTION_HEADERS = {
        "Ocp-Apim-Subscription-Key": "df273a71edc54965b55bde4de6f34a02",
    }

    def data_received(self, chunk):
        pass

    # Rewrite prepare() method to determine API invoking type
    # 'json' - client sends json in http request body
    # 'form' - client sends multpart/form-data to server
    # 'mix'  - client sends image as bytes stream in request body
    def prepare(self):
        http_method = self.request.method
        http_header = self.request.headers

        if http_method.upper() == "POST":
            if "Content-Type" in http_header:
                content_type = http_header["Content-Type"]
                print(content_type)
                if content_type.startswith("application/json"):
                    self.INVOKING_TYPE = 'json'
                elif content_type.startswith("multipart/form-data"):
                    self.INVOKING_TYPE = 'form'
                elif content_type.startswith("application/octet-stream"):
                    self.INVOKING_TYPE = 'mix'
                else:
                    self.INVOKING_TYPE = "undefined"
            else:
                self.INVOKING_TYPE = "undefined"
        print("------ {0} ------".format(self.INVOKING_TYPE))

    def check_json(self, action_type=""):
        # Return:
        # 0     - Format check failed
        # dict  - Format check succeed

        print(action_type)
        if not self.request.body:
            return 0
        else:
            try:
                message = json_decode(self.request.body)

                if action_type == "CREATE":
                    return message if "face_list_id" in message and "desc" in message else 0

                elif action_type == "DELETE" or action_type == "GET":
                    return message if "face_list_id" in message else 0
                # "REMOVE"
                else:
                    return message if "face_list_id" in message and "face_id" in message else 0
            except JSONDecodeError:
                return 0

    # ====================================
    # 'request'     - wrong request url
    # 'json'        - post with wrong json format
    # 'argument'    -
    # ====================================
    def send_error_response(self, err_type=""):
        err_text = "[edge] Undefined error"

        if err_type == "request":
            err_text = "[edge] Illegal Request"

        elif err_type == "json":
            err_text = "[edge] Illegal JSON Format"

        elif err_type == "argument":
            err_text = "[edge] Argument Error"

        elif err_type == "face_id":
            err_text = "[edge] Get Face ID Error"

        self.write(json.dumps({"error": err_text}))
        self.finish()


# ==================================================================
# PostAPIHandler only used for POST method
# * Rewrite structural post() to invoke in the subclass
# * Define a get_face_id() method to get face_id of uploaded picture
# ==================================================================

class PostHandler(BaseHandler):
    msg = {}

    @tornado.gen.coroutine
    def get_face_id(self, pic):
        url = "{0}/detect".format(self.FACE_URL)
        self.FACE_HEADERS["Content-Type"] = "application/octet-stream"
        request = HTTPRequest(url, method="POST", headers=self.FACE_HEADERS, body=pic)
        browser = AsyncHTTPClient()
        response = yield browser.fetch(request)

        face_ids = []
        if response.code == 200:
            result = json_decode(response.body)
            print(result)
            for item in result:
                face_ids.append(item["faceId"])

            return face_ids
        else:
            return face_ids

    def handle_request(self):
        pass

    def get(self):
        pass

    def post(self, action=None):
        if self.INVOKING_TYPE == "undefined":
            self.send_error_response("request")

        elif self.INVOKING_TYPE == "json":
            self.msg = self.check_json(action)
            if not self.msg:
                self.send_error_response("json")
            else:
                # THIS METHOD WILL BE OVERRIDDEN IN SUBCLASS
                self.handle_request()
        elif self.INVOKING_TYPE == "mix":
            try:
                if self.request.body:
                    self.handle_request()
                # body is empty
                else:
                    self.send_error_response("request")

            except MissingArgumentError:
                self.send_error_response("request")

        else:  # CALL_TYPE: form
            try:
                # THIS METHOD WILL BE OVERRIDDEN IN SUBCLASS
                self.handle_request()

            except MissingArgumentError:
                self.send_error_response("request")

