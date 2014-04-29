'''
Created on Apr 28, 2014

@author: Rishi Josan

This program takes a CSV of IP address block ranges (starting and ending IPs
and creates a list of all IPs. Country specific data downloaded from
http://www.nirsoft.net/countryip/cn.html
The ipaddr library is required(Warning: May not wor in Python3)
'''

import csv
from ipaddr import IPAddress

def listBetween(start, end):
    result = []
    start = IPAddress(start)
    end = IPAddress(end)
    
    while start <= end:
        result.append(str(start))
        start += 1
    return result


def readCSV():
    
    blockList = []
    with open('/media/sf_G_DRIVE/colDam/cn.csv', 'rb') as csvfile:
        ipBlocks = csv.reader(csvfile, delimiter=',')
        
        for row in ipBlocks:
            newRow=[]
            newRow.append(row[0])
            newRow.append(row[1])
            blockList.append(newRow)
    return blockList
        
        
blockList = readCSV()

ipList = []

for ipRange in blockList:
    print 'Getting IPs between ' + ipRange[0] + ' and ' + ipRange[1]
    subList = listBetween(ipRange[0], ipRange[1])
    ipList = ipList + subList
    
    