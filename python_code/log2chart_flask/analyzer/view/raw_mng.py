from flask import Flask,request,render_template,redirect,url_for
from analyzer import app
from analyzer.lib.RawMng import *
from analyzer.lib.RawProc import *
from analyzer.lib.JSON_IO import *

#=================================================================
#      Routes Begin
#=================================================================


@app.route('/upload',methods=['GET','POST'])
def upload():
    do_upload(request,app.config['DATA_PATH'])
    return redirect(url_for('raw_index'))

@app.route('/list_raw')
def list_raw():
    files = os.listdir(app.config['DATA_PATH']+'/raw')
    return render_template('raw/list_raw.html',rawList=sorted(files))


#______ Delete route ______
@app.route('/delete/<dtype>/<filename>')
def delete(dtype,filename):
    do_remove(app.config['DATA_PATH'],dtype,filename)

    return redirect(url_for(dtype+'_index'))

"""
@app.route('/delete_all_cache')
def delete_all_cache():
   os.path.walk(app.config['DATA_PATH']+'/cache',clean_all_cache,"")
   return redirect(url_for('analyzer_index'))
"""



@app.route('/process/<ptype>/<filename>')
def process_raw(ptype,filename):
    data = {} 
    cachePath = app.config['DATA_PATH']+"/cache/"+ptype+"/"
    rawFilePath = app.config['DATA_PATH']+"/raw/"+filename
    if ptype == "log":
        data = raw2log(rawFilePath)
    elif ptype == "common":
        data = raw2common(rawFilePath)
    
    json2file(cachePath,data,filename)
    return "Process Completed"

