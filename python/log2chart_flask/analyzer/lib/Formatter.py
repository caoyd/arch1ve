def dict_to_list(data):
    ###### input data looks like:
    ###### {'POST': 1, 'BAD': 4, 'HEAD': 7, 'GET': 8} 
    listData = []

    for i in data.items():
        listData.append(list(i))
    return listData
    ###### return listData looks like:
    ###### [['POST',1], 
    ######  ['BAD',4],
    ######  ['HEAD',7], 
    ######  ['GET',8]]



def dict_to_sorted_list(data,num=0):
    listData = []

    ###### data needs top x
    if num:
        tmp = sorted(data.iteritems(),key=lambda d:d[1],reverse=True)
        topIP = tmp[:num]
        for i in topIP:
            listData.append(list(i))

    ###### data only needs sorted
    else:
        tmp = sorted(data.iteritems(),key=lambda d:d[0])
        ###### the "tmp" data looks like:
        ###### [('POST': 1), ('BAD': 4), ('HEAD': 7), ('GET': 8)] 
        for i in tmp:
            listData.append(list(i))

    return listData


