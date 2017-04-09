## Your name: Samii Stoloff
## The option you've chosen: 2

# Put import statements you expect to need here!
import unittest
import sqlite3
import requests
import json
import re
import tweepy
import twitter_info

# Authentication information should be in a twitter_info file...
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# And we've provided the setup for your cache. But we haven't written any functions for you, so you have to be sure that any function that gets data from the internet relies on caching, just like in Project 2.
CACHE_FNAME = "206_final_cache.json"
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}


# Define your function get_user_tweets here:

def get_user_tweets(user):
	twit_user = "twitter_{}".format(user) 
	if twit_user in CACHE_DICTION:
		print(user)
		pass
	else:
		print(user)
		results = api.user_timeline(user) 
		CACHE_DICTION[twit_user] = results 
		f = open(CACHE_FNAME,'w') 
		f.write(json.dumps(CACHE_DICTION)) 
		f.close() 
	return CACHE_DICTION[twit_user]

# Write your test cases here.


## Remember to invoke all your tests...