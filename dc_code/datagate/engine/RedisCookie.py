import redis
import os.path
import logging.config
import tornado.web
from tornado.httpclient import HTTPError
from tornado.escape import json_decode


class RedisCookie(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

        # Initialize logger
        logging.config.fileConfig(os.path.join(self.settings["config_path"], "logger_conf.ini"))
        self.logger = logging.getLogger("datagateLogger")

        # Initialize redis connection
        self.redis_conn = redis.StrictRedis(**dict(self.settings["config"]["rediscookie"]))

    def data_received(self, chunk):
        pass

    def get(self, *args):
        try:
            key = args[0]
            if key:
                cookie = self.redis_conn.get(key)
                if cookie:
                    self.logger.info("Cookie found: {}".format(cookie))
                    self.write(cookie)
                else:
                    self.logger.info("Cookie not found")
                    self.write("no cookie")
        except tornado.web.HTTPError:
            self.write("[GET] error")

    def post(self, *args):
        try:
            key = args[0]
            self.redis_conn.delete(key)
            post_data = json_decode(self.request.body)
            self.redis_conn.set(key, post_data["cookie"])
        except KeyError:
            self.write("[POST] error")
