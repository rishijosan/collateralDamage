'''
Created on Mar 25, 2014

@author: Rishi Josan
'''

import requests, json, base64, dns.message
from StringIO import StringIO
import os
import cPickle as pickle

key_createMeasurement = os.getenv('ripeCreateMeasurement')
key_editMeasurement = os.getenv('ripeEditMeasurement')
key_getProbeInfo = os.getenv('ripeGetProbeInfo')
key_getRes = os.getenv('ripeGetRes')


createLink = 'https://atlas.ripe.net/api/v1/measurement/?key=' + key_createMeasurement
headers = {'content-type': 'application/json'}

#target = ['87.105.250.3','209.244.0.3', '208.67.222.222' ]


targetIps = []
ipPrefix = '203.119.35.'

for i in range(100):
    
    target = ipPrefix + str(i)
    targetIps.append(target)
    

##########################################    DEFINITIONS    ##############################################################
definitions = []

for i in range(len(targetIps)):

    def1 = {}
    
    #Core Description Properties
    def1['target'] =  targetIps[i]
    def1['description'] =  'Rishi_Find_Lemon_CN ' + str(i)
    def1['type'] =  'dns'
    def1['af'] =  4
    def1['is_oneoff'] =  True
    
    #DNS Specific Properties
    def1['query_class'] =  'IN'
    def1['query_type'] =  'A'
    def1['query_argument'] =  'www.facebook.com'
    def1['recursion_desired'] =  True
    def1['protocol'] =  'UDP'
    
    definitions.append(def1)


defIo = StringIO()
json.dump(definitions,defIo)
##########################################    END  OF DEFINITIONS    ##############################################################



##########################################    PROBES    ##############################################################
probes = []


#for i in range(3):

probe1 = {}
#Core Description Properties
probe1['requested'] =  10
probe1['type'] =  'country'
probe1['value'] =  'cn'
probes.append(probe1)




probeIo = StringIO()
json.dump(probes,probeIo)
##########################################    END  OF PROBES    ##############################################################

#createPingJson = { 'definitions': [ { 'target': 'ripe.net', 'description': 'My First Measurement', 'type': 'ping', 'af': 4 } ], 'probes': [ { 'requested': 50, 'type': 'area', 'value': 'WW' } ] }


createDNSJson = {}
createDNSJson['definitions'] = definitions
createDNSJson['probes']= probes


req = requests.post(createLink, data=json.dumps(createDNSJson), headers=headers)
measurement = req.json().get('measurements')

#Save list of measurements
with open('/media/sf_G_DRIVE/measurementsCN.pk', 'wb') as output:
    pickle.dump(measurement, output, protocol=0)
