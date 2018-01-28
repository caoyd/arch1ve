# -*- coding: utf-8 -*-
from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch()

result = es.search(index="cdfund", size=100, body={
    "query": {
        "term": {"title": u"联名卡" }
    }
})

print(result)


