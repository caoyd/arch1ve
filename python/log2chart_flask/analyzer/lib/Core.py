from JSON_IO import *
from Formatter import *
from RawProc import *



def get_log_analysis(dataPath,aType,filename):
    ###### aType: per_hour, req_method, status_code, top_ip
    cachePath = dataPath+'/cache'
    fileCachePath = cachePath+'/log/'+filename
    data = file2json(fileCachePath)
    dictData = data[aType]
        
    listData = []
    if aType == 'per_hour':
        listData = dict_to_sorted_list(dictData)
    elif aType == 'top_ip':
        listData = dict_to_sorted_list(dictData,10)
    else:
        listData = dict_to_list(dictData)

    return json.dumps(listData)
    # This data can be used in highchart directly
        
    

def get_common_analysis(dataPath,aType,filename):
    cachePath = dataPath+'/cache'
    fileCachePath = cachePath+'/common/'+filename
    data = file2json(fileCachePath)
    dictData = data[aType]

    listData = []
    listData = dict_to_list(dictData)
    return json.dumps(listData)
        




