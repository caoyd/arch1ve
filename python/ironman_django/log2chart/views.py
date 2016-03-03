import os

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View

from .engine.Core import *
from .engine.Utils import *



class IndexView(View):
    def get(self,request):
        return render(request,'log2chart/index.html')


def data_list(request):
    files = os.listdir(os.path.join(settings.LOG_FILE_DIR,"data"))
    dataList = sorted(files)
    context = {
        'dataList': dataList
    }
    return render(request,'log2chart/data_list.html',context)



def upload2extract(request):
    fileObj = request.FILES['uploader']
    filename = fileObj.name
    uploadPath = os.path.join(settings.LOG_FILE_DIR,"temp")
    filePath = os.path.join(uploadPath,filename)
    with open(filePath,'wb') as upfile:
        upfile.write(fileObj.read())

    data = {}
    logPath = settings.LOG_FILE_DIR
    dataPath = logPath+"/data/"
    tempFile = logPath+"/temp/"+filename
    data = raw2log(tempFile)
    json2file(dataPath,data,filename)
    os.remove(tempFile)

    return HttpResponseRedirect('/log2chart/')



def delete(request,filename):
    dataPath = settings.LOG_FILE_DIR
    os.remove(dataPath+'/data/'+filename)
    return HttpResponse('deleted')



def renderer(request,filename,atype):
    return render(request,'log2chart/renderer.html')



def chart(request,filename,atype):
    #logAType = ['per_hour','req_method','status_code','top_ip']
    dataPath = os.path.join(settings.LOG_FILE_DIR,"data")
    data = data2chart(dataPath,filename,atype)

    context = {
        'data': data,
        'filename': filename,
    }
    return render(request,'log2chart/chart/'+atype+'.html',context)
    # data - contains data which highchart needs to build chart
    # filename - filename displays on top of chart in red


