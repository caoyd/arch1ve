import os
import os.path
import sys

import tornado.web
import tornado.httpserver
import tornado.ioloop

# from configparser import ConfigParser

from engine.wechat.Wechat import Wechat
from engine.common.Handlers import DebugHandler
from engine.common.Handlers import DefaultHandler


class MRobot(tornado.web.Application):
    def __init__(self):
        BASE = os.path.dirname(__file__)
        # Initialize main configuration from 'conf/config.ini'
        # conf = ConfigParser()
        # conf.read(os.path.join(BASE, "conf/config.ini"))

        handlers = [
            # (r"/api/wechat", Wechat),
            # (r"/api/wechat", WechatHandshake),
            (r"/debug", DebugHandler),
        ]

        settings = dict(
            # config=conf,
            default_handler_class=DefaultHandler,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            # static_path=os.path.join(os.path.dirname(__file__), "static"),
            # upload_path=os.path.join(os.path.dirname(__file__), "upload"),
            config_path=os.path.join(os.path.dirname(__file__), "conf"),
            xsrf_cookies=False,
            cookie_secret="__WITH_GREAT_POWER_COMES_WITH_GREAT_RESPONSIBILITY__",
            debug=True,
            autoreload=False,
        )

        super().__init__(handlers, **settings)


if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) > 1 else 8000

    http_srv = tornado.httpserver.HTTPServer(MRobot())
    http_srv.listen(port)
    tornado.ioloop.IOLoop.current().start()
