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
import collections
import itertools

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
CACHE_FNAME = "206_final_cache.json"
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}


# # Define your function get_user_tweets here:

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


# Caching twitter info about a movie	
# Enables you to search for a title of a movie and find the tweets that include the name of the movie.

def get_twitter_info(twitter_info):
	search_twitter = "twitter_{}".format(twitter_info)
	if search_twitter in CACHE_DICTION:
		print ("using cached data for", twitter_info)
		print ("\n")
		twitter_results = CACHE_DICTION[search_twitter]
	else:
		print ("getting data from internet for", twitter_info)
		print ("\n")
		twitter_results = api.twitter_info(q = twitter_info)
		CACHE_DICTION[search_twitter] = twitter_results
		f = open(CACHE_FNAME, 'w')
		f.write(json.dumps(CACHE_DICTION))
		f.close()
		
	tweets = twitter_results['statuses']
	return tweets

# Pull data from OMDb API and cache it
# Takes an input of a movie name and returns a dictionary of info about the movie, caches, and returns the cache file.

def get_movie_info(movie_info):
	search_movie = "OMBb_{}".format(movie_info)
	if search_movie in CACHE_DICTION:
		print ("Using cached data for", movie_info)
		print("\n")
		movie_dictionary = CACHE_DICTION[search_movie]
	else:
		print ("getting data for", movie_info)
		print ("\n")
		baseurl = 'http://www.omdbapi.com/?'
		url_params = {'t': movie_info}
		response = requests.get(baseurl, params = url_params)
		movie_dictionary = response.json()
		CACHE_DICTION[search_movie] = movie_dictionary
		f = open(CACHE_FNAME, 'w')
		f.write(json.dumps(CACHE_DICTION))
		f.close()

	return movie_dictionary

print (json.dumps(get_movie_info("Frozen"), indent = 2))

t_connect = sqlite3.connect('stoloff_final.db')
t_cursor = t_connect.cursor()

t_cursor.execute('DROP TABLE IF EXISTS stoloff_final')

# create table for tweets
c_table = 'CREATE TABLE IF NOT EXISTS '
c_table += 'Tweets (tweet_id TEXT PRIMARY KEY, '
c_table += 'tweet_text TEXT, twitter_user TEXT, movie_association TEXT, retweet_num INTEGER, favorite_num INTEGER)'

t_cursor.execute(c_table)

# create table for users
c_table = 'CREATE TABLE IF NOT EXISTS '
c_table += 'Users (user_id TEXT PRIMARY KEY, '
c_table += 'user_handle TEXT, user_favorites INTEGER)'

t_cursor.execute(c_table)

# create table for movies
c_table = 'CREATE TABLE IF NOT EXISTS '
c_table += 'Movies (movie_id TEXT PRIMARY KEY, ' #The movie ID will be the primary key
c_table += 'movie_title TEXT, director TEXT, rating INTEGER, lead_actor_m TEXT, lead_actor_f TEXT)'

t_cursor.execute(c_table)


statement_1 = 'INSERT OR IGNORE INTO Tweets VALUES (?, ?, ?, ?, ?, ?)'
statement_2 = 'INSERT OR IGNORE INTO Users VALUES (?, ?, ?)'
statement_3 = 'INSERT OR IGNORE INTO Movies VALUES (?, ?, ?, ?, ?, ?)'


class Movie():
	def __init__(self, movie_dictionary):
		self.movie_id = movie_dictionary['imdbID']
		self.movie = movie_dictionary
		self.title = movie_dictionary['Title']
		self.year = movie_dictionary['Year']
		self.director = movie_dictionary['Director']
		self.rating = movie_dictionary['imdbRating']

	def get_actor_names(self):
		actor_names = self.movie['Actors']
		return actor_names

	def create_movie_table(self):
		actor_names = Movie.get_actor(self)
		actor_list = actor_names.split(", ")
		lead_role = actor_list[0]
		t = self.movie_id, self.title, self.director, self.rating, lead_role

	def __str__(self):
		return self.title + " stars the actors " + self.get_actor_names + " and was driected by " + self.director + " in " + self.year ".  It has an IMDB rating of " + self.rating + "."



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