import re
#______ raw data convert ______
def raw2log(rawData):
    perHourDict = {}
    topIPDict = {}
    reqMethodDict = {}
    statusCodeDict = {}
    access = {}

    ipPTN       = re.compile('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    timePTN     = re.compile('\[(.*)\]')
    httpCodePTN = re.compile('\s(\d\d\d)\s')
    requestPTN  = re.compile('"([A-Z]{3,7})\s')
    
    with open(rawData,'r') as log:
        for line in log.readlines():

    #==========================================
    #  Different log format different process |
    #==========================================
            ###### extract IP addr
            match = ipPTN.search(line)
            if match:
                ip = match.group(1)
                if ip in topIPDict:
                    topIPDict[ip] += 1
                else:
                    topIPDict[ip] = 1
           
            ###### extract hour from timestamp 
            match = timePTN.search(line)
            if match:
                hour = match.group(1).split(':')[1]
                if hour in perHourDict:
                    perHourDict[hour] += 1
                else:
                    perHourDict[hour] = 1

            ###### extract request method
            match = requestPTN.search(line)
            if match:
                reqMethod = match.group(1)
                if reqMethod not in ['GET','HEAD','POST','PUT','DELETE','OPTIONS','TRACE','CONNECT']:
                    reqMethod = 'BAD'
                if reqMethod in reqMethodDict:
                    reqMethodDict[reqMethod] += 1
                else:
                    reqMethodDict[reqMethod] = 1
                
            ###### extract http code
            match = httpCodePTN.search(line)
            if match:
                statusCode = match.group(1)
            if statusCode in statusCodeDict:
                statusCodeDict[statusCode] += 1
            else:
                statusCodeDict[statusCode] = 1
    
            

    #+----------------------------------------+
    #  Different log format different process |
    #+----------------------------------------+
    access["top_ip"] = topIPDict
    access["per_hour"] = perHourDict
    access["req_method"] = reqMethodDict
    access["status_code"] = statusCodeDict

    return access



def raw2common(rawData):
    simpleDict = {}
    general = {}
    
    with open(rawData,'r') as raw:
        for line in raw.readlines():
            line = line.rstrip('\n')
            line = line.rstrip('\r')
            tmp = line.split(':')
            simpleDict[tmp[0]] = int(tmp[1])

    general["simple"] = simpleDict

    return general
