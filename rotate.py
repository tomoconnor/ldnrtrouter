#!/usr/bin/env python
import redis
from datetime import datetime
MAXLEN=800
DB = redis.StrictRedis(host='localhost',port=6379, db=0)
length_In = DB.hlen('speedIn')
suffix = str(datetime.now().day) + "_" + str(datetime.now().month)

if length_In >= MAXLEN:
	DB.rename('speedIn',"speedIn_%s" % suffix)
	DB.rename('speedOut',"speedOut_%s" % suffix)
	print "Rotated database tables to %s" % suffix
else:
	print "Files not big enough to rotate"

