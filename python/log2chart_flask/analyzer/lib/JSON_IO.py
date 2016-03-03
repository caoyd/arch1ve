import json

def file2json(dataFile):
    with open(dataFile,'r') as f:
        jsonObj = json.load(f)
        #______ return json object,it will be used in highcharts _______

        #return json.dumps(tmp)
        return jsonObj

def json2file(cachePath,data,filename):
    path = cachePath+filename
    print path
    with open(path,'w') as f:
        json.dump(data,f)
