#!/usr/bin/env python

import sys
import tweepy

import redis
CONSUMER_KEY = '8OJelKAlxsIrMeJs0Vdw'
CONSUMER_SECRET = 'ZQUFWIa6Wxfo4riUIiUknO2agHaEJieN6oQBwDg5Jo'
ACCESS_KEY = '722384634-hA6H6RjYzstzmyS2VMHqGor9tWPTM3knufsNA40N'
ACCESS_SECRET = 'GYIl0EzcIDgCEATYSkYM3nt2iA383ajxJURHyeNYg'
def sendTweet(text):
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)
	api.update_status(text)

if __name__ == "__main__":
	DB = redis.StrictRedis(host='localhost',port=6379, db=0)
	speedInLatest = DB.get('speedInLatest')
	speedOutLatest = DB.get('speedOutLatest')
	tweet = "Current Hackathon Internet traffic: In: %s Out: %s" % (speedInLatest, speedOutLatest)
	print tweet
	sendTweet(tweet)

