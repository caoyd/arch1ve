import os
import os.path
import codecs
import json
import logging
import logging.config
import redis
import redis.exceptions
import tornado.web
import tornado.httpserver
import tornado.ioloop
from configparser import ConfigParser
from engine.MySQLGate import MySQLGate
from engine.RedisGate import RedisCD
from engine.RedisCookie import RedisCookie


class DataGate(tornado.web.Application):
    def __init__(self):
        base_path = os.path.dirname(__file__)
        # Initialize database configuration from conf/db.ini
        conf = ConfigParser()
        conf.read(os.path.join(base_path, "conf/db.ini"))

        # Initialize logger
        logging.config.fileConfig(os.path.join(base_path, "conf/logger_conf.ini"))
        tornado_logger = logging.getLogger("TornadoLogger")

        # Initialize small data into cache
        try:
            redis_conn = redis.StrictRedis(**dict(conf["rediscd"]))
            data2cache_path = os.path.join(base_path, "data2cache/cd")
            for file in os.listdir(data2cache_path):
                if file.startswith('.'):
                    continue

                filename = file.split('.')[0]
                # with codecs.open(os.path.join(data2cache_path, file), 'r', 'utf-8') as f:
                with open(os.path.join(data2cache_path, file), 'r') as f:
                    tmp = json.load(f)
                    redis_conn.set(filename, json.dumps(tmp))
        except redis.exceptions.ConnectionError:
            logging.error("error connecting redis server")

        handlers = [
            (r"/mysql", MySQLGate),
            (r"/rediscd", RedisCD),
            (r"/api_cookie/(.*)", RedisCookie),
        ]

        settings = dict(
            config=conf,
            logger=tornado_logger,
            config_path=os.path.join(os.path.dirname(__file__), "conf"),
            xsrf_cookies=False,
            cookie_secret="__WITH_GREAT_POWER_COMES_WITH_GREAT_RESPONSIBILITY__",
            debug=True,
            autoreload=False,
        )

        super().__init__(handlers, **settings)

if __name__ == "__main__":
    DEFAULT_PORT = 9527
    http_srv = tornado.httpserver.HTTPServer(DataGate())
    http_srv.listen(DEFAULT_PORT)
    tornado.ioloop.IOLoop.current().start()
