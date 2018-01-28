import os
import os.path
import sys
import logging
import logging.config
from configparser import ConfigParser

import tornado.web
import tornado.httpserver
import tornado.ioloop

from engine.common.Handlers import DefaultHandler
from engine.common.MySQLHandler import MySQLHandler
from engine.common.RedisHandler import RedisHandler

from engine.baidu.Cosmetic import Cosmetic
from engine.baidu.Drug import Drug
from engine.baidu.ExchangeRate import ExchangeRate
from engine.baidu.Lottery import Lottery
from engine.baidu.PhoneNo import PhoneNo

from engine.service_cd.NightWork import NightWork
from engine.service_cd.AirQuality import AirQuality
from engine.service_cd.Manufacturer import Manufacturer
from engine.service_cd.AssociateConstructor import AssociateConstructor
from engine.service_cd.Barcode import Barcode
from engine.service_cd.FileInfo import FileInfo
from engine.service_cd.FoodDrugAdmin import FoodDrugAdmin
from engine.service_cd.Invoice import InvoiceCaptcha, InvoiceCheck
from engine.service_cd.PreForSale import PreForSale
from engine.service_cd.RealEstateSrvOrg import RealEstateCaptcha, RealEstateHandler
from engine.service_cd.TaxiFound import TaxiFound
from engine.service_cd.TaxiLostFound import LostFoundCaptcha, LostFound, LostFoundRecord
from engine.service_cd.DisabilityCert import DisabilityCertCaptcha, DisabilityCert

from engine.service_cq.DesignatedMedical import DesignatedMedical
from engine.service_cq.SocialSecurity import SocialSecurity

from engine.service_gy.PublicInterest import PublicInterest
from engine.service_gy.SocialService import HelpPost, PraisePost, WeeklyReport


class Plug(tornado.web.Application):
    def __init__(self):
        base_path = os.path.dirname(__file__)
        # Initialize main configuration from 'conf/conf.ini'
        conf = ConfigParser()
        conf.read(os.path.join(base_path, "conf/conf.ini"))

        # Initialize logger
        logging.config.fileConfig(os.path.join(base_path, "conf/logger_conf.ini"))
        tornado_logger = logging.getLogger("TornadoLogger")

        handlers = [
            # =====================================
            #              API for CD
            # =====================================

            # Service API with crawled data stored in Redis
            (r"/api/waterfee", RedisHandler),
            (r"/api/gasfee", RedisHandler),
            (r"/api/welfarehouse", RedisHandler),
            (r"/api/subordinateorg", RedisHandler),
            (r"/api/corporeitymoni", RedisHandler),

            # Service API crawl data directly
            (r"/api/aq", AirQuality),
            (r"/api/manufacturer", Manufacturer),
            (r"/api/fileinfo", FileInfo),
            (r"/api/barcode", Barcode),
            (r"/api/preforsale", PreForSale),
            (r"/api/constructor", AssociateConstructor),
            (r"/api/invoicecaptcha", InvoiceCaptcha),
            (r"/api/invoicecheck", InvoiceCheck),
            (r"/api/realestatecaptcha", RealEstateCaptcha),
            (r"/api/realestate", RealEstateHandler),
            (r"/api/lostfoundcaptcha", LostFoundCaptcha),
            (r"/api/lostfound", LostFound),
            (r"/api/lostfoundrecord", LostFoundRecord),
            (r"/api/taxifound", TaxiFound),
            (r"/api/fda/food/(.*)", FoodDrugAdmin),
            (r"/api/fda/foodinspect/(.*)", FoodDrugAdmin),
            (r"/api/fda/healthfood/(.*)", FoodDrugAdmin),
            (r"/api/fda/cosmetic/(.*)", FoodDrugAdmin),
            (r"/api/fda/drug/(.*)", FoodDrugAdmin),
            (r"/api/disabilitycertcaptcha", DisabilityCertCaptcha),
            (r"/api/disabilitycert", DisabilityCert),

            # Baidu API
            (r"/api/baidu/cosmetic", Cosmetic),
            (r"/api/baidu/phone", PhoneNo),
            (r"/api/baidu/exchangerate/(.*)", ExchangeRate),
            (r"/api/baidu/drug", Drug),
            (r"/api/baidu/lottery/(.*)", Lottery),

            (r"/api/nightwork", NightWork),
            # Wildcard for CD
            (r"/api/(.*)", MySQLHandler),


            # =====================================
            #              API for CQ
            # =====================================

            (r"/api_cq/dm/(.*)", DesignatedMedical),
            (r"/api_cq/ss/(.*)", SocialSecurity),
            (r"/api_cq/(.*)", MySQLHandler),

            # =====================================
            #              API for GY
            # =====================================
            (r"/api_gy/publicinterest", PublicInterest),
            (r"/api_gy/helppost", HelpPost),
            (r"/api_gy/praisepost", PraisePost),
            (r"/api_gy/weeklyreport", WeeklyReport),


        ]

        settings = dict(
            config=conf,
            logger=tornado_logger,
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

        super(Plug, self).__init__(handlers, **settings)


if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) > 1 else 8000
    http_srv = tornado.httpserver.HTTPServer(Plug())
    http_srv.listen(port)
    tornado.ioloop.IOLoop.current().start()
