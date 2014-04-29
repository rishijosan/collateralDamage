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
    
    jsonList = []
    for meas in measurements:
        newLink = 'https://atlas.ripe.net/api/v1/measurement/' + str(meas) + '/result/'
        req = requests.get(newLink, headers=headers)
        resSet = req.json()
        jsonList.append(resSet)             

    with open('/media/sf_G_DRIVE/colDam/jsonListCN.pk', 'wb') as output:
        pickle.dump(jsonList, output, protocol=0)

    return jsonList

#Parse result JSON to extract DNS Responses
def parseResults(resSet):
    dnsMessageList = [] #Complete DNS Message Response
    respList = [] #List which stores dst_addr, from, src_addr and resolved IP
        
    for meas in resSet:
        for probe in meas:
            if probe.has_key('result'): 
                respRow = []
                abuf = probe.get('result').get('abuf')
                dnsMessage = dns.message.from_wire(base64.b64decode(abuf))
                dnsMessageList.append(dnsMessage)
                
                respRow.append(probe['dst_addr'])
                respRow.append(probe['from'])
                respRow.append(probe['src_addr'])
                respRow.append(IPFromMessage(dnsMessage))
                respList.append(respRow)
        
    return dnsMessageList, respList

#Decode abuf 
def decode(abuf):
    print dns.message.from_wire(base64.b64decode(abuf))

#Create a set of Unique IPs received for a set of measurements    
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
with open('/media/sf_G_DRIVE/colDam/measurementsCN.pk', 'rb') as inp:
    measList = pickle.load(inp)
    
#Load previously saved jsonList
with open('/media/sf_G_DRIVE/colDam/jsonListCN.pk', 'rb') as inp:
    jsonList = pickle.load(inp)
    
#jsonList = getRes(measList)
#dnsResp,respList = parseResults(jsonList)

measList = ['1636768']
jsonList = getRes(measList)
dnsResp,respList = parseResults(jsonList)
lemonIps = getUniqueIps(dnsResp)




#print str(responses[6].answer[0][0])