'''
Created on Mar 25, 2014

@author: Rishi Josan
'''

import requests, json, base64, dns.message
from StringIO import StringIO
import os
import cPickle as pickle
import time

key_createMeasurement = os.getenv('ripeCreateMeasurement')
key_editMeasurement = os.getenv('ripeEditMeasurement')
key_getProbeInfo = os.getenv('ripeGetProbeInfo')
key_getRes = os.getenv('ripeGetRes')


createLink = 'https://atlas.ripe.net/api/v1/measurement/?key=' + key_createMeasurement
headers = {'content-type': 'application/json'}
typeMeas = 'dns' # 'dns'


#Manually Creating Target IPs
def manualTarget():
    targetIps = []
    
    if typeMeas == 'dns':
        ipPrefix = '203.119.35.'
        for i in range(100):
            target = ipPrefix + str(i)
            targetIps.append(target)
           
    if typeMeas == 'tr':
        targetIps.append('203.119.35.100')
    return targetIps
        
        

#Function to create Measurement Definitions
def createDef(targetIps, iterNo):
    definitions = []
    
    for i in range(len(targetIps)):
    
        def1 = {}
        
        #Core Description Properties
        def1['target'] =  targetIps[i]
        def1['af'] =  4
        def1['is_oneoff'] =  True
        
        
        #DNS Specific Properties
        if typeMeas == 'dns':
            def1['type'] =  'dns'
            def1['description'] =  'Rishi_Bulk_IN_US_XXX' + str(iterNo) + '_'+ str(i)
            def1['query_class'] =  'IN'
            def1['query_type'] =  'A'
            def1['query_argument'] =  'xxx.com'
            def1['recursion_desired'] =  True
            def1['protocol'] =  'UDP'
        
        #Traceroute Specific Properties
        if typeMeas == 'tr':
            def1['description'] =  'Rishi_tracert_IR_CN ' + str(i)
            def1['type'] =  'traceroute' 
            def1['protocol'] = 'ICMP' #UDP
            
        
        
        definitions.append(def1)
    
    
    defIo = StringIO()
    json.dump(definitions,defIo)
    return definitions



#Function to create Probes
def createProbes():
    probes = []
    
    probe1 = {}
    
    if typeMeas == 'dns':
        #Core Description Properties
        probe1['requested'] =  500
        probe1['type'] =  'country'
        probe1['value'] =  'us'
        probes.append(probe1)
        
    if typeMeas == 'tr':
        probe1['requested'] =  1
        probe1['type'] =  'probes'
        probe1['value'] =  '12464'
        probes.append(probe1)
    
    
    probeIo = StringIO()
    json.dump(probes,probeIo)
    return probes


#createPingJson = { 'definitions': [ { 'target': 'ripe.net', 'description': 'My First Measurement', 'type': 'ping', 'af': 4 } ], 'probes': [ { 'requested': 50, 'type': 'area', 'value': 'WW' } ] }

measList = []
createDNSJson = {}

#List of measurements
with open('/media/sf_G_DRIVE/colDam/IN_IPs.pk', 'rb') as inp:
    subList = pickle.load(inp)

createDNSJson['probes']= createProbes()


'''
This function was supposed to create measurements in bulk, as RIPE Atlas does not allow more
than 100 concurrent measurements, we cannot create them in bulk
'''
for i in  range(1):
    print 'Creating  measurements ' + str(i) + 'for IPs' + str(i*100) + ' to ' + str(i*100 +100)
    createDNSJson['definitions'] = createDef(subList[2*100:2*100+100],1) #Replace number by i
    req = requests.post(createLink, data=json.dumps(createDNSJson), headers=headers)
    
    measurement = req.json().get('measurements')
    measList.append(measurement)
    print 'Waiting'
    time.sleep(10)


#Save list of measurements
with open('/media/sf_G_DRIVE/bulkMeas1.pk', 'wb') as output:
    pickle.dump(measList, output, protocol=0)
    
    


