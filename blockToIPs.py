'''
Created on Apr 28, 2014

@author: Rishi Josan

This program takes a CSV of IP address block ranges (starting and ending IPs
and creates a list of all IPs. Country specific data downloaded from
http://www.nirsoft.net/countryip/cn.html
The ipaddr library is required(Warning: May not work in Python3)
'''

import csv
from ipaddr import IPAddress
import random
import pickle

def listBetween(start, end):
    result = []
    start = IPAddress(start)
    end = IPAddress(end)
    
    
    while start <= end:
        result.append(str(start))
        start += 1
    return result

#Read CSV File and Create list of Start and End IP. IMP : Empty Lines at the end must be deleted!
def readCSV():
    
    blockList = []
    with open('/media/sf_G_DRIVE/colDam/in.csv', 'rb') as csvfile:
        ipBlocks = csv.reader(csvfile, delimiter=',')
        
        for row in ipBlocks:
            newRow=[]
            newRow.append(row[0])
            newRow.append(row[1])
            blockList.append(newRow)
    return blockList


def get24Between(start, end):
    result = []
    startArr = start.split('.')
    endArr = end.split('.')
    
    for i in range( int(startArr[0]),int(endArr[0])+1 ):
        for j in range( int(startArr[1]),int(endArr[1])+1 ):
            for k in range( int(startArr[2]),int(endArr[2])+1 ):
                result.append(str(i) + '.' + str(j) + '.' + str(k) + '.' + str(random.randint(0,255)) )
    
    
    return result



#newList = get24Between('2.144.0.0','2.147.255.255')
#subList = listBetween('5.10.160.0', '5.10.191.255')

        
blockList = readCSV()
ipList = []

for ipRange in blockList:
    print 'Getting IPs between ' + ipRange[0] + ' and ' + ipRange[1]
    #subList = listBetween(ipRange[0], ipRange[1])
    subList = get24Between(ipRange[0],ipRange[1])
    ipList = ipList + subList


myfile = open('/media/sf_G_DRIVE/colDam/IN_IPs.csv', 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
wr.writerow(ipList)
myfile.close()


with open('/media/sf_G_DRIVE/IN_IPs.pk', 'wb') as output:
    pickle.dump(ipList, output, protocol=0)
    