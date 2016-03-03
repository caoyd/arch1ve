from flask import Flask

app = Flask(__name__)
DATA_PATH = app.root_path+'/data'
DEBUG = True
app.config.from_object(__name__)

from analyzer.view import *
