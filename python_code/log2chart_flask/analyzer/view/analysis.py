import os
from flask import Flask,request,render_template,redirect,url_for
from analyzer import app
from analyzer.lib.Core import *

@app.route('/list_cache/<ctype>')
def list_cache(ctype):
    cachePath = app.config['DATA_PATH']+"/cache/"+ctype
    caches = os.listdir(cachePath)
    return render_template('analysis/list_cache.html',cacheList=sorted(caches),cacheType=ctype)


@app.route('/renderer/<aType>/<filename>')
def renderer(aType,filename):
    # "aType" and "filename" will be used in JS(window.location.href)
    url = ""
    if aType in ['simple']:
        url = "common_index"
    elif aType in ['per_hour','req_method','status_code','top_ip']:
        url = "log_index"

    return render_template('analysis/renderer.html',backLink=url)
    # "analyzer/router.html" - ajax loader used to load highchart JS


@app.route('/load_chart/<aType>/<filename>')
def load_chart(aType,filename):
    commonAType = ['simple']
    logAType = ['per_hour','req_method','status_code','top_ip']

    if aType == 'simple':
        data = get_common_analysis(app.config['DATA_PATH'],aType,filename)
    else:
        data = get_log_analysis(app.config['DATA_PATH'],aType,filename)

    return render_template('analysis/atype/'+aType+'.html',data=data,filename=filename)
    # data - contains data which highchart needs to build chart
    # filename - filename displays on top of chart in red
    
