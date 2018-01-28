import os,os.path
from werkzeug import secure_filename

######def clean_all_cache(arg,dirs,files):
######    for f in files:
######        fullPath = os.path.join(dirs,f)
######        if os.path.isfile(fullPath):
######            os.remove(fullPath)
######
######def clean_file_cache(arg,dirs,files):
######    for f in files:
######        fullPath = os.path.join(dirs,f)
######        if os.path.isdir(fullPath):
######            continue
######        else:
######            if f == arg:
######                os.remove(fullPath)

def do_remove(dataPath,dtype,filename):
    if dtype == 'raw':
        os.remove(dataPath+'/raw/'+filename)
        #os.path.walk(dataPath+'/cache',clean_file_cache,filename)
    else:
        os.remove(dataPath+'/cache/'+dtype+'/'+filename)
        #os.path.walk(dataPath+'/cache',clean_file_cache,filename)


def do_upload(request,dataPath):
    if request.method == 'POST':
        file = request.files['fileUploader']
        if file:
            filename = secure_filename(file.filename)
            file.save(dataPath+'/raw/'+filename)
