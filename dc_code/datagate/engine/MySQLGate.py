import json
import mysql.connector
import tornado.web
from mysql.connector.errors import InterfaceError, ProgrammingError
from tornado.escape import json_decode


class MySQLGate(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

        # Configure mysql connection
        self.msg = dict()
        self.config_name = ""
        self.mysql_conf = dict()
        self.mysql_conn = mysql.connector.MySQLConnection()

        # Initialize logger
        self.logger = self.settings["logger"]

    def data_received(self, chunk):
        pass

    def prepare(self):
        # Retrieve msg from request body
        self.msg = json_decode(self.request.body)
        self.config_name = "mysql" + self.msg["city"]

        self.mysql_conf = dict(self.settings["config"][self.config_name])

    def post(self):
        try:
            self.do_process_logic()

        except InterfaceError:
            self.logger.error("Error happened while connecting mysql")
            self.write("error")
        except ProgrammingError:
            self.logger.error("MySQL error")
            self.write("error")

    def do_process_logic(self):
        # Initialize connection
        self.mysql_conn.connect(**self.mysql_conf)

        self.logger.info("[DATAGATE {}]  {}".format(self.config_name.upper(), self.msg["sql"]))

        cursor = self.mysql_conn.cursor()
        cursor.execute(self.msg["sql"])
        # Get column names
        col_names = cursor.column_names

        result = []
        # result = [
        #   {"id":1, "name": "Ted", "age":30},
        #   {"id":2, "name": "Skipper", "age":31}
        #   ...
        # ]
        for record in cursor:
            # zip column names and record into dict
            result.append(dict(zip(col_names, record)))
        self.write(json.dumps(result))
        cursor.close()

    def on_finish(self):
        self.mysql_conn.close()
