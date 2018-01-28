import os
import os.path
import sys
from configparser import ConfigParser

import tornado.ioloop

from engine.common.Handlers import DefaultHandler

from engine.vision.Emotion import Emotion
from engine.vision.Face import Face
from engine.vision.Match import Match


class HTTPApplication(tornado.web.Application):
    def __init__(self):
        BASE = os.path.dirname(__file__)
        # Initialize main configuration from 'conf/config.ini'
        conf = ConfigParser()
        conf.read(os.path.join(BASE, "conf/config.ini"))

        handlers = [
            # (r"/debug", DebugHandler),

            # Microsoft cognitive service
            (r"/vision/face", Face),
            (r"/vision/emotion", Emotion),
            (r"/vision/match", Match),


            # (r"/facelist", FaceListHandler),
            # (r"/facelist/create", FaceListCreateHandler),
            # (r"/facelist/delete", FaceListDeleteHandler),
            # (r"/facelist/get", FaceListGetHandler),
            # (r"/facelist/add", FaceAddHandler),
            # (r"/facelist/remove", FaceRemoveHandler),
            # (r"/vision/detect", FaceDetectHandler),
            # (r"/vision/match", FaceMatchHandler),
        ]

        settings = dict(
            config=conf,
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
    DEFAULT_PORT = 8000
    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = DEFAULT_PORT

    http = HTTPApplication()
    http.listen(port)
    tornado.ioloop.IOLoop.current().start()
