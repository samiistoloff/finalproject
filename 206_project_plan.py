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
# consumer_key = twitter_info.consumer_key
# consumer_secret = twitter_info.consumer_secret
# access_token = twitter_info.access_token
# access_token_secret = twitter_info.access_token_secret
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)

# # Set up library to grab stuff from twitter with your authentication, and return it in a JSON format 
# api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# # And we've provided the setup for your cache. But we haven't written any functions for you, so you have to be sure that any function that gets data from the internet relies on caching, just like in Project 2.
# CACHE_FNAME = "206_final_cache.json"
# try:
# 	cache_file = open(CACHE_FNAME,'r')
# 	cache_contents = cache_file.read()
# 	cache_file.close()
# 	CACHE_DICTION = json.loads(cache_contents)
# except:
# 	CACHE_DICTION = {}


# # Define your function get_user_tweets here:

# def get_user_tweets(user):
# 	twit_user = "twitter_{}".format(user) 
# 	if twit_user in CACHE_DICTION:
# 		print(user)
# 		pass
# 	else:
# 		print(user)
# 		results = api.user_timeline(user) 
# 		CACHE_DICTION[twit_user] = results 
# 		f = open(CACHE_FNAME,'w') 
# 		f.write(json.dumps(CACHE_DICTION)) 
# 		f.close() 
# 	return CACHE_DICTION[twit_user]

# Write your test cases here.

class Test_Cases(unittest.TestCase):
	def test_tweet_cache(self):
		fname = open("SI206_finalproject_cache.json", "r").read()
		self.assertTrue("tweets" in fname)
	def test_movie_cache(self):
		fname = open("SI206_finalproject_cache.json", "r").read()
		self.assertTrue("movies" in fname)
	def test_get_user_tweets(self):
		dict_type = get_user_tweets("amy adams")
		self.assertEqual(type(dict_type), type([12, "some", "words"]))
	def test_get_user_tweets_2(self):
		user_tweet = get_user_tweets("amy adams")
		self.assertEqual(type(user_tweet[1]), type({}))
	def test_movie_string(self):
		string_movie = Movie(movie_diction)
		self.assertEqual(type(string_movie.__str__(), str))
	def test_movie_title(self):
		movie_title = Movie(movie_diction)
		self.assertEqual(type(movie_title.title), type("The Godfather"))
	def test_get_actor(self):
		actor_name = Movie(movie_diction)
		self.assertEqual(type(actor_name.get_actor()), type(['Ashton']))
	def test_actors_tweets(self):
		actor_tweet = Movie(movie_diction)
		actor_name = actor_tweets.get_actor()[0]
		actor_info = get_user_tweets(actor_name)
		self.assertEqual(actor_info[1]['user']['twitter_handle'], actor_name)
	

## Remember to invoke all your tests...

if __name__ == "__main__":
	unittest.main(verbosity=2)