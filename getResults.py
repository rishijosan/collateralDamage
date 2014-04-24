'''
Created on Apr 23, 2014

@author: Rishi Josan
'''

import requests, json, base64, dns.message
import cPickle as pickle

headers = {'content-type': 'application/json'}



#Retrieve List of IP message from a DNS Response
def IPFromMessage(dnsMess):
    ipList = []
    for entry in dnsMess.answer:
        for subEntry in entry:
            ipList.append(str(subEntry))
    return ipList


#Get results for a list of measurements
def getRes(measurements):
    respList = []
    dnsMessageList = []
    jsonList = []
    
    for meas in measurements:
        
        newLink = 'https://atlas.ripe.net/api/v1/measurement/' + str(meas) + '/result/'
        
        req = requests.get(newLink, headers=headers)
        resSet = req.json()
        
        jsonList.append(resSet)
        
        for item in resSet:
            if item.has_key('result'): 
                respRow = []
                abuf = item.get('result').get('abuf')
                dnsMessage = dns.message.from_wire(base64.b64decode(abuf))
                dnsMessageList.append(dnsMessage)
                
                respRow.append(item['dst_addr'])
                respRow.append(item['from'])
                respRow.append(item['src_addr'])
                respRow.append(IPFromMessage(dnsMessage))
                respList.append(respRow)
                


    with open('/media/sf_G_DRIVE/jsonListCN.pk', 'wb') as output:
        pickle.dump(jsonList, output, protocol=0)

    return dnsMessageList, respList, jsonList

def decode(abuf):
    print dns.message.from_wire(base64.b64decode(abuf))
    
def getUniqueIps(dnsResp):
    ipSet = set()
    
    for resp in dnsResp:
        for entry in resp.answer:
            for subEntry in entry:
                ipSet.add(str(subEntry))
            
            
    with open('/media/sf_G_DRIVE/colDam/lemonIps.pk', 'wb') as output:
        pickle.dump(ipSet, output, protocol=0)
    
    return ipSet
   
   
    
#List of measurements
with open('/media/sf_G_DRIVE/measurementsCN.pk', 'rb') as inp:
    measList = pickle.load(inp)
    
dnsResp,respList,jsonList = getRes(measList)
lemonIps = getUniqueIps(dnsResp)




#print str(responses[6].answer[0][0])