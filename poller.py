#/usr/bin/env python

import subprocess as sp
import re
import redis
from time import sleep

STRING = re.compile(r'STRING:\s+(.+)$')
COUNTER32 = re.compile(r'Counter32:\s(.+)$')
DB = redis.StrictRedis(host='localhost',port=6379, db=0)
C="astound"
R="192.168.6.1"
MIN=0
MAX=1024000
MAX=104857600
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
	eth1In = getSNMPCounter(C,'iso.3.6.1.2.1.2.2.1.10.2',R)
        eth1Out = getSNMPCounter(C,'iso.3.6.1.2.1.2.2.1.16.2',R)
	
	sleep(30)
	eth0In_ = getSNMPCounter(C,'iso.3.6.1.2.1.2.2.1.10.1',R)
	eth0Out_ = getSNMPCounter(C,'iso.3.6.1.2.1.2.2.1.16.1',R)
	eth1In_ = getSNMPCounter(C,'iso.3.6.1.2.1.2.2.1.10.2',R)
        eth1Out_ = getSNMPCounter(C,'iso.3.6.1.2.1.2.2.1.16.2',R)
	
	eth0InDelta = eth0In_ - eth0In
	eth0OutDelta = eth0Out_ - eth0Out
	
	eth1InDelta = eth1In_ - eth1In
	eth1OutDelta = eth1Out_ - eth1Out

#	print eth0name, eth0InDelta
#	print eth0name, eth0OutDelta
	
#	print eth1name, eth1InDelta
#	print eth1name, eth1OutDelta

	gk_eth0In_jsonblob = """
{ "item" : "%s",
  "max" : { "text" : "Max value",
      "value" : "%s"
    },
  "min" : { "text" : "Min value",
      "value" : "0"
    }
}
	""" % (eth0InDelta,MAX)

	gk_eth0Out_jsonblob = """
{ "item" : "%s",
  "max" : { "text" : "Max value",
      "value" : "%s"
    },
  "min" : { "text" : "Min value",
      "value" : "0"
    }
}
	""" %(eth0OutDelta,MAX)

	st_eth0In_jsonblob = """

{ "item" : [ { "text" : "",
        "value" : %s
      },
      { "text" : "",
        "value" : %s
      }
    ] }
	""" %(eth0In,eth0In_)
	st_eth0Out_jsonblob = """

{ "item" : [ { "text" : "",
        "value" : %s 
      },
      { "text" : "",
        "value" : %s
      }
    ] }
	""" %(eth0Out,eth0Out_)

	
	open("tmp/gk_eth0Out.json",'w').write(gk_eth0Out_jsonblob)
	open("tmp/gk_eth0In.json",'w').write(gk_eth0In_jsonblob)
	sp.check_output("scp -q -i uploadkey tmp/gk_eth0Out.json ldnrt@ec2-23-20-146-112.compute-1.amazonaws.com:/var/www/", shell=True, stderr=sp.STDOUT)
	sp.check_output("scp -q -i uploadkey tmp/gk_eth0In.json ldnrt@ec2-23-20-146-112.compute-1.amazonaws.com:/var/www/", shell=True, stderr=sp.STDOUT)

	open("tmp/st_eth0Out.json",'w').write(st_eth0Out_jsonblob)
	open("tmp/st_eth0In.json",'w').write(st_eth0In_jsonblob)
	sp.check_output("scp -q -i uploadkey tmp/st_eth0Out.json ldnrt@ec2-23-20-146-112.compute-1.amazonaws.com:/var/www/", shell=True, stderr=sp.STDOUT)
	sp.check_output("scp -q -i uploadkey tmp/st_eth0In.json ldnrt@ec2-23-20-146-112.compute-1.amazonaws.com:/var/www/", shell=True, stderr=sp.STDOUT)



