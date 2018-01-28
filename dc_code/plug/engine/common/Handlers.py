import json
import socket
import tornado.web
import tornado.httpclient
from json.decoder import JSONDecodeError
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPError
from tornado.web import MissingArgumentError


class DefaultHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("404")

    def post(self):
        self.write("404")


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        # Read main configuration from Tornado settings
        self.config = self.settings["config"]
        # Get logger from Tornado settings
        self.logger = self.settings["logger"]

        # Initialize AsyncHTTPClient
        self.browser = AsyncHTTPClient()
        # Setup default page size
        self.default_page_size = int(self.config["global"]["PAGE_SIZE"])

    def init_paging_param(self, page, page_size):
        page = int(float(page)) if len(page) else 1
        page_size = int(float(page_size)) if len(page_size) else self.default_page_size
        # Make sure page and page_size are positive int
        page = 1 if page < 1 else page
        page_size = self.default_page_size if page_size < 0 else page_size

        page = (page - 1) * page_size
        return page, page_size

    # ==================================
    # success=1: send success response
    # success=0: send error response
    # ==================================
    def send_json_response(self, data, success=1):
        if success:
            # Check whether the list is empty or not
            if len(data):
                ret_code = "000000"
                ret_msg = "本次请求成功"
                result = data
            # Data is empty, send failed response,
            # Response message is read from config
            else:
                ret_code = "000001"
                ret_msg = self.config["error"]["NO_RESULT_ERR"]
                result = []

        else:
            ret_code = "000001"
            ret_msg = data
            result = []

        template = {
            "head": {
                "rtnCode": ret_code,
                "rtnMsg": ret_msg
            },
            "body": {
                "results": result
            }
        }

        self.set_header("Content-Type", "application/json;charset=utf-8")
        self.set_header("Access-Control-Allow-Origin", "*")
        # Display Chinese in result
        self.write(json.dumps(template, ensure_ascii=False))
        self.finish()

    def data_received(self, chunk):
        pass

    def post(self):
        pass


class SpiderHandler(BaseHandler):
    async def get(self, *args):
        try:
            await self.do_process_logic(*args)
            # await self.do_process_logic(*args)

        except MissingArgumentError as err:
            self.logger.error("[{0}]: {1}".format(self.__class__, str(err)))
            self.send_json_response(self.config["error"]["MISSING_ARG_ERR"], 0)
        except (HTTPError, socket.gaierror, OSError) as err:
            self.logger.error("[{0}]: {1}".format(self.__class__, str(err)))
            self.send_json_response(self.config["error"]["SIMPLE_ERR"], 0)
        except JSONDecodeError:
            self.logger.error("[{0}]: {1}".format(self.__class__, "JSON decode error"))
            self.send_json_response(self.config["error"]["SIMPLE_ERR"], 0)
        except ValueError as err:
            self.logger.error("[{0}]: {1}".format(self.__class__, str(err)))
            self.send_json_response(self.config["error"]["SIMPLE_ERR"], 0)
        except KeyError as err:
            self.logger.error("[{0}]: {1}".format(self.__class__, str(err)))
            self.send_json_response(self.config["error"]["SIMPLE_ERR"], 0)

    # Inherit this method and put API Code here
    async def do_process_logic(self, *args):
        pass


class DataHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

        # Initialize datagate(for MySQL access)
        self.mysql_url = self.config["urls"]["MYSQL"]
        self.redis_url = self.config["urls"]["REDIS"]

    # ==================================
    # Asynchronous method to access MWay
    # return a flag and  a result list
    # flag = 0: success
    # flag = 1: fail
    # ==================================
    async def fetch_data(self, msg):
        url = ""
        if "sql" in msg:
            url = self.mysql_url
        elif "key" in msg:
            url = self.redis_url

        request = HTTPRequest(url, method="POST", body=json.dumps(msg))
        try:
            response = await self.browser.fetch(request)
            result = json.loads(response.body.decode("utf-8"))
            return 0, result
        # Can not connect to datagate
        except (ConnectionRefusedError, socket.gaierror):
            self.logger.error("[{0}]: {1}".format(self.__class__, "Fail to connect datagate"))
            return 1, []
        except tornado.httpclient.HTTPError:
            self.logger.error("[{0}]: {1}".format(self.__class__, "tornado.httpclient.HTTPError in DataHandler"))
            return 1, []
        # Datagate return "error" string
        except JSONDecodeError:
            self.logger.error("[{0}]: {1}".format(self.__class__, "Datagate return error"))
            return 1, []

