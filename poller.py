#/usr/bin/env python

import subprocess as sp
import json
import re
import redis
from time import sleep
from time import time
from utils import binary_prefix,bitrate


STRING = re.compile(r'STRING:\s+(.+)$')
COUNTER32 = re.compile(r'Counter32:\s(.+)$')
DB = redis.StrictRedis(host='localhost',port=6379, db=0)
C="public"
R="192.168.100.1"
MIN=0
#MAX=1024000
#MAX=104857600
#MAX=104857600

def getSNMPString(community,oid,host):
	cmd = "/usr/bin/snmpget -v2c -c%s %s %s" %( community,host,oid)	
	output = sp.check_output(cmd,shell=True)
	value = STRING.search(output).group(1)
	return value

def getSNMPCounter(community,oid,host):

	cmd = "/usr/bin/snmpget -v2c -c%s %s %s" %( community,host,oid)	
        output = sp.check_output(cmd,shell=True)
        value = COUNTER32.search(output).group(1)
        return int(value)

if __name__ == "__main__":
	eth0name = "FastEthernet 0/0" #getSNMPString(C,'iso.3.6.1.2.1.2.2.1.2.1',R)
	eth1name = "FastEthernet 0/1" #getSNMPString(C,'iso.3.6.1.2.1.2.2.1.2.2',R)

	ts = int(time())
	
	eth0In = getSNMPCounter(C,'iso.3.6.1.2.1.2.2.1.10.1',R)
	eth0Out = getSNMPCounter(C,'iso.3.6.1.2.1.2.2.1.16.1',R)
	

	print eth0In
	print eth0Out
	sleep(1)
	eth0In_p= getSNMPCounter(C,'iso.3.6.1.2.1.2.2.1.10.1',R)
	eth0Out_p = getSNMPCounter(C,'iso.3.6.1.2.1.2.2.1.16.1',R)
	
	eth0InDelta = eth0In_p - eth0In
	eth0OutDelta = eth0Out_p - eth0Out
	DB.hset('speedIn',ts,eth0InDelta)
	DB.set('speedInLatest',bitrate(binary_prefix(eth0InDelta)))
	DB.hset('speedOut',ts,eth0OutDelta)
	DB.set('speedOutLatest',bitrate(binary_prefix(eth0OutDelta)))
	print binary_prefix(eth0InDelta)
	print binary_prefix(eth0OutDelta)


