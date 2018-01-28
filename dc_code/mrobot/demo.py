import time
import sched
from threading import Timer
import xml.etree.ElementTree as ET
import hashlib
import jieba

text = "工信处女干事每月经过下属科室都要亲口交代24口交换机等技术性器件的安装工作"


time_interval = 1


def hello():
    print("yo~")

t = Timer(time_interval, hello)
t.start()

