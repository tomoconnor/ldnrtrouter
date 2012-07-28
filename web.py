
#/usr/bin/env python
import subprocess as sp
import json
import re
import redis
from time import sleep
from time import time
from utils import binary_prefix
from jinja2 import Environment, FileSystemLoader
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)
DB = redis.StrictRedis(host='localhost',port=6379, db=0)
MAXIn=DB.hlen('speedIn')
MAXOut=DB.hlen('speedOut')
print MAXIn
use_values = {}

allIn = DB.hgetall('speedIn')
allOut = DB.hgetall('speedOut')

ds1 = ""
for key in sorted(allIn.iterkeys()):
	ds1 += "{ x: %s, y: %s }," % (key,allIn[key])
	
ds2 = ""
for key in sorted(allOut.iterkeys()):
	ds2 += "{ x: %s, y: %s }," % (key,allOut[key])

use_values['dataseries1'] = ds1
use_values['dataseries2'] = ds2
use_values['dataseries1_name'] = 'Speed In'
use_values['dataseries2_name'] = 'Speed Out'



env = Environment(loader=FileSystemLoader('webroot/templates'))
template = env.get_template('routergraph.tpl')
outputfile = open('webroot/core.html','w')
outputfile.write(template.render(use_values))
outputfile.flush()
outputfile.close()
