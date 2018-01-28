"""
Inheritance:
tornado.web.RequestHandler
    BaseHandler
        SpiderHandler
            AirQuality
            Barcode
            ...
        DataHandler
            MySQLHandler
            RedisHandler
"""
import os
import json
import logging.config
import tornado.web
import tornado.httpclient
from json.decoder import JSONDecodeError
from socket import gaierror
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPError
from tornado.web import MissingArgumentError


# Add page placeholder to SQL statement
def paginate(sql):
    return "{0} LIMIT {{}}, {{}}".format(sql)


class DebugHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("debug.html")


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
        # ==================================================
        # Initialize log configuration from conf/logging.ini
        # Use self.settings["config_path"] to get root path
        # ==================================================
        logging.config.fileConfig(os.path.join(self.settings["config_path"], "logging.ini"))
        self.logger = logging.getLogger("plugLogger")
        # Initialize AsyncHTTPClient like a browser
        self.browser = AsyncHTTPClient()

    # ============================================
    # success=1: send success response(default)
    # success=0: send error response
    # ============================================
    def send_json_response(self, data, success=1):
        if success:
            # Data is not empty, send success response
            if len(data):
                ret_code = "000000"
                ret_msg = "本次请求成功"
                result = data
            # Data is empty, send failed response,
            # and response message is read from config
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
    USER_AGENTS = [
        "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; MI NOTE LTE Build/KTU84P) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.4 TBS/025489 Mobile Safari/533.1 MicroMessenger/6.3.13.49_r4080b63.740 NetType/cmnet Language/zh_CN",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
        "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; MI NOTE LTE Build/KTU84P) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.4 TBS/025489 Mobile Safari/533.1 MicroMessenger/6.3.13.49_r4080b63.740 NetType/cmnet Language/zh_CN",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13D15 MicroMessenger/6.3.13 NetType/WIFI Language/zh_CN",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Shuame; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.9.1.1000 Chrome/39.0.2146.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
        "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13",
        "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 6.0b; Windows 98)",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)",
        "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8",
        "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)",
        "Opera/9.20 (Windows NT 6.0; U; en)",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Shuame; .NET4.0C; .NET4.0E; GWX:RED)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2716.0 Safari/537.36 OPR/39.0.2234.0 (Edition developer)Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2716.0 Safari/537.36 OPR/39.0.2234.0 (Edition developer)",
    ]

    async def get(self, *args):
        try:
            await self.do_process_logic(*args)

        except MissingArgumentError as err:
            self.logger.error("[{0}]: {1}".format(self.__class__, str(err)))
            self.send_json_response(self.config["error"]["MISSING_ARG_ERR"], 0)
        except (HTTPError, gaierror, OSError) as err:
            self.logger.error("[{0}]: {1}".format(self.__class__, str(err)))
            self.send_json_response(self.config["error"]["SIMPLE_ERR"], 0)
        except JSONDecodeError:
            self.logger.error("[{0}]: {1}".format(self.__class__, "JSON decode error"))
            self.send_json_response(self.config["error"]["SIMPLE_ERR"], 0)

    # Inherit this method and put API Code here
    async def do_process_logic(self, *args):
        pass


class DataHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

        # Initialize datagate(for MySQL access)
        self.mysql = self.config["urls"]["MYSQL"]
        self.redis = self.config["urls"]["REDIS"]
        # Setup default page size
        self.default_page_size = int(self.config["global"]["PAGE_SIZE"])

    # ===================================
    # According to user's query argument,
    # format pager parameter for paginate
    # ===================================
    def init_paging_param(self, page, page_size):
        page = int(float(page)) if len(page) else 1
        page_size = int(float(page_size)) if len(page_size) else self.default_page_size
        # Make sure page and page_size are positive int
        page = 1 if page < 1 else page
        page_size = self.default_page_size if page_size < 0 else page_size

        page = (page - 1) * page_size
        return page, page_size

    # ===================================
    # Asynchronous method to access MWay
    # return a 'flag' and a 'result list'
    # flag = 0: success
    # flag = 1: fail
    # ===================================
    async def fetch_data(self, msg):
        url = ""
        if "sql" in msg:
            url = self.mysql
        elif "key" in msg:
            url = self.redis

        request = HTTPRequest(url, method="POST", body=json.dumps(msg))
        try:
            response = await self.browser.fetch(request)
            result = json.loads(response.body.decode("utf-8"))
            return 0, result
        # Can not connect to datagate
        except ConnectionRefusedError:
            self.logger.error("[{0}]: {1}".format(self.__class__, "Fail to connect datagate"))
            return 1, []
        except tornado.httpclient.HTTPError:
            self.logger.error("[{0}]: {1}".format(self.__class__, "tornado.httpclient.HTTPError in DataHandler"))
            return 1, []
        # Datagate return "error" string
        except JSONDecodeError:
            self.logger.error("[{0}]: {1}".format(self.__class__, "Datagate return error"))
            return 1, []

