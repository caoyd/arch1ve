from flask import Flask,request,render_template,redirect,url_for
from analyzer import app

##########################
###### Routes Begin ######
##########################

#______ Basic Route ______
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/raw')
def raw_index():
    return render_template('raw/raw_index.html')


@app.route('/common')
def common_index():
    return render_template('analysis/analysis_index.html',headLine="Common Data")

@app.route('/log')
def log_index():
    return render_template('analysis/analysis_index.html',headLine="Access Log")

@app.route('/map')
def map_index():
    return render_template('analyzer/analyzer_index.html')

