#/usr/bin/env python

import subprocess as sp
import json
import re
import redis
from time import sleep
from time import time

STRING = re.compile(r'STRING:\s+(.+)$')
COUNTER32 = re.compile(r'Counter32:\s(.+)$')
DB = redis.StrictRedis(host='localhost',port=6379, db=0)
C="astound"
R="192.168.6.1"
MIN=0
#MAX=1024000
#MAX=104857600
#MAX=104857600
#MAX=26214400
cnt_in = DB.llen('eth0In')
cnt_out = DB.llen('eth0Out')
v_in = DB.lrange('eth0In',0,cnt_in)
v_out = DB.lrange('eth0Out',0,cnt_out)
v_in_max = max(v_in)
v_out_max = max(v_out)
TrueMax = int(max([v_in_max,v_out_max]))
MAX = (TrueMax+500)


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
	eth0name = getSNMPString(C,'iso.3.6.1.2.1.2.2.1.2.1',R)
	eth1name = getSNMPString(C,'iso.3.6.1.2.1.2.2.1.2.2',R)

	eth0In = getSNMPCounter(C,'iso.3.6.1.2.1.2.2.1.10.1',R)
	eth0Out = getSNMPCounter(C,'iso.3.6.1.2.1.2.2.1.16.1',R)
	#eth1In = getSNMPCounter(C,'iso.3.6.1.2.1.2.2.1.10.2',R)
        #eth1Out = getSNMPCounter(C,'iso.3.6.1.2.1.2.2.1.16.2',R)
	
	sleep(10)
	eth0In_ = getSNMPCounter(C,'iso.3.6.1.2.1.2.2.1.10.1',R)
	eth0Out_ = getSNMPCounter(C,'iso.3.6.1.2.1.2.2.1.16.1',R)
	#eth1In_ = getSNMPCounter(C,'iso.3.6.1.2.1.2.2.1.10.2',R)
        #eth1Out_ = getSNMPCounter(C,'iso.3.6.1.2.1.2.2.1.16.2',R)
	
	eth0InDelta = eth0In_ - eth0In
	eth0OutDelta = eth0Out_ - eth0Out

	DB.lpush("eth0Out",eth0OutDelta)
	DB.lpush("eth0In", eth0InDelta)

	cnt_out = int(DB.llen('eth0Out'))	
	cnt_in = int(DB.llen('eth0In'))
	print cnt_out, cnt_in
	stop = max([cnt_out, cnt_in]) - 200
	print stop
	v_out = DB.lrange('eth0Out',stop,cnt_out)
	v_in = DB.lrange('eth0In', stop, cnt_in)
	
	toJson_out = {"item":v_out, 
	"settings": {
	     "axisx": [
	      "3min",
	      "2min",
	      "1min"
	     ],
	     "axisy": [
	      str(MIN),
	      str(MAX)
	     ],
	     "colour": "ff9900"
	    }
	}
	toJson_in = {"item":v_in, 
	"settings": {
	     "axisx": [
	      "3min",
	      "2min",
	      "1min"
	     ],
	     "axisy": [
	      str(MIN),
	      str(MAX)
	     ],
	     "colour": "ff9900"
	    }
	}
	open("tmp/li_eth0Out.json",'w').write(json.dumps(toJson_out))
	open("tmp/li_eth0In.json",'w').write(json.dumps(toJson_in))

	sp.check_output("scp -q -i uploadkey tmp/li_eth0Out.json ldnrt@webcam.wibblesplat.com:/var/www/", shell=True, stderr=sp.STDOUT)
	sp.check_output("scp -q -i uploadkey tmp/li_eth0In.json ldnrt@webcam.wibblesplat.com:/var/www/", shell=True, stderr=sp.STDOUT)




