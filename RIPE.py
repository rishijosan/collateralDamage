'''
Created on Mar 25, 2014

@author: Rishi Josan
'''

import requests, json, base64, dns.message
from StringIO import StringIO
import os




key_createMeasurement = os.getenv('ripeCreateMeasurement')

key_editMeasurement = os.getenv('ripeEditMeasurement')

key_getProbeInfo = os.getenv('ripeGetProbeInfo')

key_getRes = os.getenv('ripeGetRes')


createLink = 'https://atlas.ripe.net/api/v1/measurement/?key=' + key_createMeasurement
headers = {'content-type': 'application/json'}

target = '87.105.250.3'

##########################################    DEFINITIONS    ##############################################################
definitions = []
def1 = {}

#Core Description Properties
def1['target'] =  target
def1['description'] =  'DNS_API_TWEET'
def1['type'] =  'dns'
def1['af'] =  4
def1['is_oneoff'] =  True

#DNS Specific Properties
def1['query_class'] =  'IN'
def1['query_type'] =  'A'
def1['query_argument'] =  'www.twitter.com'
def1['recursion_desired'] =  True
def1['protocol'] =  'UDP'

definitions.append(def1)
defIo = StringIO()
json.dump(definitions,defIo)
##########################################    END  OF DEFINITIONS    ##############################################################



##########################################    PROBES    ##############################################################
probes = []
probe1 = {}

#Core Description Properties
probe1['requested'] =  15
probe1['type'] =  'country'
probe1['value'] =  'cl'



probes.append(probe1)
probeIo = StringIO()
json.dump(probes,probeIo)
##########################################    END  OF PROBES    ##############################################################

#createPingJson = { 'definitions': [ { 'target': 'ripe.net', 'description': 'My First Measurement', 'type': 'ping', 'af': 4 } ], 'probes': [ { 'requested': 50, 'type': 'area', 'value': 'WW' } ] }


createDNSJson = {}
createDNSJson['definitions'] = definitions
createDNSJson['probes']= probes


req = requests.post(createLink, data=json.dumps(createDNSJson), headers=headers)
measurement = req.json().get('measurements')[0]

measurement = '1598006'
#1598006
#1598012

#getResLink = 'https://atlas.ripe.net/api/v1/measurement/' + measurement + '/result/?key=' + key_getRes
newLink = 'https://atlas.ripe.net/api/v1/measurement/' + str(measurement) + '/result/'

req = requests.get(newLink, headers=headers)
resSet = req.json()

for item in resSet:
    abuf = item.get('result').get('abuf')
    dnsMessage = dns.message.from_wire(base64.b64decode(abuf))
    print dnsMessage
    print ""


    
    


