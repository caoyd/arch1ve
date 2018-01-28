import json
import os.path
import redis
import logging.config
import tornado.web
from tornado.escape import json_decode


def in_range(num, r):
    start, end = tuple(r)

    # The end is '-1'
    if end == -1:
        if num >= start:
            return True
        else:
            return False
    else:
        if start <= num <= end:
            return True
        else:
            return False


class RedisCD(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        # Initialize logger
        logging.config.fileConfig(os.path.join(self.settings["config_path"], "logger_conf.ini"))
        self.logger = logging.getLogger("datagateLogger")

    def data_received(self, chunk):
        pass

    def post(self):
        redis_db_name = os.path.basename(self.request.path)
        redis_conn = redis.StrictRedis(**dict(self.settings["config"][redis_db_name]))

        # Get message from request body
        msg = json_decode(self.request.body)

        # Retrieve key from 'msg'
        key = msg["key"]
        self.logger.info("[DATAGATE {}]  Accessing Redis key: {}".format(redis_db_name.upper(), key))

        if 'filter' in msg:
            raw = redis_conn.get(key)
            tmp = json.loads(raw.decode("utf-8"))
            items = []
            for item in tmp:
                if in_range(msg["filter"], item["range"]):
                    items.append(item)

            resp = json.dumps(items)
        else:
            data = redis_conn.get(key)
            resp = data.decode('utf-8')

        self.write(resp)

