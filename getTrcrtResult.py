'''
Created on Apr 28, 2014

@author: Rishi Josan
'''


import requests, json, base64, dns.message
import cPickle as pickle
import os


key_createMeasurement = os.getenv('ripeCreateMeasurement')

createLink = 'https://atlas.ripe.net/api/v1/measurement/?key=' + key_createMeasurement

headers = {'content-type': 'application/json'}


def getTraceRes():
    meas = '1638460'
    newLink = 'https://atlas.ripe.net/api/v1/measurement/' + str(meas) + '/result/'
    req = requests.get(newLink, headers=headers)
    resSet = req.json()
    
    route = []
    
    for res in resSet[0]['result']:
        if res['result'][0].has_key('from'):
            route.append(res['result'][0]['from'])
            
    return route
    
    
#
'''
Now send DNS queries to each IP to get point of injection
Create DNS measurements with target IPs as traceroute queries and probe as initial probe no.
'''

def createDefs(targetIps):
    definitions = []
    
    for i in range(len(targetIps)):
    
        def1 = {}
        
        #Core Description Properties
        def1['target'] =  str(targetIps[i])
        def1['af'] =  4
        def1['is_oneoff'] =  True
        
        
        #DNS Specific Properties
        def1['type'] =  'dns'
        def1['description'] =  'Rishi_DNS_From_TrcRt ' + str(i)
        def1['query_class'] =  'IN'
        def1['query_type'] =  'A'
        def1['query_argument'] =  'www.facebook.com'
        def1['recursion_desired'] =  True
        def1['protocol'] =  'UDP'
              
        definitions.append(def1)
    
    return definitions
      
      
        
def createProbes():
    probes = []

    probe1 = {}

    probe1['requested'] =  1
    probe1['type'] =  'probes'
    probe1['value'] =  '12464'
    probes.append(probe1)
    return probes


createDNSJson = {}

route = getTraceRes()
createDNSJson['definitions'] = createDefs(route[1:8])
createDNSJson['probes']= createProbes()


req = requests.post(createLink, data=json.dumps(createDNSJson), headers=headers)
measurement = req.json().get('measurements')

