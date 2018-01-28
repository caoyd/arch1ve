# -*- coding: utf-8 -*-
import mysql.connector
from datetime import datetime
from elasticsearch import Elasticsearch

# print(datetime.now())
mysql_conf = {
    "host": "192.168.86.86",
    "port": 3306,
    "user": "root",
    "password": "hello",
    "database": "excavator",
}
mysql_conn = mysql.connector.MySQLConnection()
mysql_conn.connect(**mysql_conf)

mysql_cursor = mysql_conn.cursor()
mysql_cursor.execute("select * from cd_fund")
# print(mysql_cursor.column_names)

es = Elasticsearch()
for record in mysql_cursor:
    qid = record[0]
    qtitle = record[1]
    es.index(index="cdfund", doc_type="text", id=qid, body={"title": qtitle, "timestamp": datetime.now()})




