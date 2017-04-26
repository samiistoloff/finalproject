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
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# # Set up library to grab stuff from twitter with your authentication, and return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

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
		
	tweets = twitter_results['tweets']
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

#print (json.dumps(get_movie_info("21 Jump Street"), indent = 2))

t_connect = sqlite3.connect('stoloff_final.db')
t_cursor = t_connect.cursor()

t_cursor.execute('DROP TABLE IF EXISTS stoloff_final')

# create table for tweets
c_table = 'CREATE TABLE IF NOT EXISTS '
c_table += 'Tweets (tweet_id TEXT PRIMARY KEY, '
c_table += 'tweet_text TEXT, user_id TEXT, twitter_user TEXT, movie_association TEXT, retweet_num INTEGER, favorite_num INTEGER)'

t_cursor.execute(c_table)

# create table for users
c_table = 'CREATE TABLE IF NOT EXISTS '
c_table += 'Users (user_id TEXT PRIMARY KEY, '
c_table += 'user_handle TEXT, user_favorites INTEGER)'

t_cursor.execute(c_table)

# create table for movies
c_table = 'CREATE TABLE IF NOT EXISTS '
c_table += 'Movies (movie_id TEXT PRIMARY KEY, ' #The movie ID will be the primary key
c_table += 'movie_title TEXT, director TEXT, rating INTEGER, lead_actor TEXT)'

t_cursor.execute(c_table)


statement_1 = 'INSERT OR IGNORE INTO Tweets VALUES (?, ?, ?, ?, ?, ?, ?)'
statement_2 = 'INSERT OR IGNORE INTO Users VALUES (?, ?, ?)'
statement_3 = 'INSERT OR IGNORE INTO Movies VALUES (?, ?, ?, ?, ?)'


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
		actor_names = Movie.get_actor_names(self)
		actor_list = actor_names.split(", ")
		lead_role = actor_list[0]
		movie_t = self.movie_id, self.title, self.director, self.rating, lead_role
		return movie_t

	def __str__(self):

		return self.title + " was directed by " + self.director  +" with notable actors being " + self.get_actors() + ". This movie had an IMDM rating of " + str(self.rating) + " and a box office performance of " + self.box_office + ". It was created in " + str(self.languages) + " language(s) and came out in " + str(self.year) + "."

movie_titles = ["21 Jump Street", "La La Land", "A Dog's Purpose", "Zootopia"]

movie_dictionary = []
for title in movie_titles: 
	movie_dictionary.append(get_movie_info(title))

movie_instance = []
for movie in movie_dictionary:
	movie_instance.append(Movie(movie))


for i in movie_instance:
	t_cursor.execute(statement_1, i.create_movie_table())

class Search_Twitter():
	def __init__(self, tweet, movie):
		self.tweet = tweet
		self.userid = tweet['user']['id_str']
		self.id = tweet['id_str']
		self.text = tweet['text']
		self.retweets = tweet['retweet_count']
		self.screen_name = tweet['user']['screen_name']
		self.associated_movie = movie
		self.favorites = tweet['favorite_count']
		self.user_favorites = tweet["user"]["favourites_count"]


	def create_twitter_table(self):

		table_1 = self.userid, self.id, self.text, self.associated_movie, self.retweets, self.favorites

		return table_1

	def create_users_table(self):

		table_2 = self.userid, self.screen_name, self.user_favorites

		return table_2


twitter_hashtags = ['#21jumpstreet', '#lalaland', '#adogspurpose', '#zootopia' ]

t_hashtags = []
for hashtag in twitter_hashtags:
	t_hashtags.append(get_twitter_data(hashtag))

twitter_instance = []
for t in range(len(t_hashtags)):
	for tweet in t_hashtags[t]:
		twitter_instance.append(Search_Twitter(tweet, movies[t]))


for i in twitter_instance:
	cur.execute(statement_1, inst.create_twitter_table())
	cur.execute(statement_2, inst.create_users_table())

for tweets in t_hashtags:
	for t in tweets:
		for u in t['entities']['user_mentions']:
			unique_identifier = "user_{}".format(u['screen_name'])
			if unique_identifier in CACHE_DICTION:
				var_t = CACHE_DICTION[unique_identifier]
			else:
				var_t = api.get_user(u['screen_name'])
				CACHE_DICTION[unique_identifier] = var_t
				f = open(CACHE_FNAME, 'w')
				f.write(json.dumps(CACHE_DICTION))
				f.close()
			table_2 = (var_t['id_str'], var_t['screen_name'], var_t['favourites_count'])
			cur.execute(statement_2, table_2)

conn.commit()

file_summary = open("206_final_project_summary.txt", 'w')
file_summary.write("SI 206 Final Project Summary\n\n")
file_summary.write("I used data analytics on four different movies to see what was being said on Twitter about them.  This project summary will allow you to compare the different movies based on a variety of statistics. \n\nThe movies I chose to compary were 21 Jump Street, La La Land, A Dog's Purpose, and Zootopia. Each movie was searched on Twitter with their respective hashtags")


statement = 'SELECT screen_name, associated_movie, num_retweets, user_favorites FROM Tweets INNER JOIN Users ON Tweets.user_id = Users.user_id WHERE num_retweets > 100 AND user_favorites > 100'
result = cur.execute(statement)
most_popular_rt_faves = {r[0]:(r[1],r[2],r[3]) for r in result.fetchall()}

user_tweets_str = "\nHere are tweets that have over 100 retweets and favorites from the specific movies I searched.  \n"

file_summary.write(user_tweets_str)

for key in most_popular_rt_faves.keys():

	file_summary.write("\n")

	file_summary.write("User: " + key + "\n Associated Movie: " +str(most_popular_rt_faves[key][0]) + "\n User Favorites: " + str(most_popular_rt_faves[key][1]) + "\n Number of Tweet Retweets: " + str(most_popular_rt_faves[key][2]))

	file_summary.write("\n")

statement = 'SELECT * FROM Tweets WHERE num_retweets > 25'
result = cur.execute(statement)
rt_tweets = []
for r in result.fetchall():
	rt_tweets.append(r)

movie_rts = {}
for tweet in rt_tweets:
	if tweet[3] not in movie_rts:
		movie_rts[tweet[3]] = tweet[4]
	else:
		movie_rts[tweet[3]] += tweet[4]
file_summary.write("\n\nFor each movie, the number of retweets \n")
for title in movie_rts.keys():
	file_summary.write(title + " Retweets: " + str(movie_rts[title]))
	file_summary.write("\n")


sort_movie_rt = sorted(movie_rts, key = lambda x: movie_rts[x], reverse = True)

top_movie_rt = [sort_movie_rt[0], movie_rts[sort_movie_rt[0]]]


file_summary.write("\nThe three most tweeted about movies are: " + str(top_movie_rt[0]) + " with " +str(top_movie_rt[1]) + " retweets\n")


statement = 'SELECT lead_actor FROM Movies'
result = cur.execute(statement)
movie_leads = {r[0] for r in result.fetchall()}

file_summary.write("\nFrom each movies, here are the lead actors:\n")

for lead in movie_leads:
	file_summary.write(lead)
	file_summary.write("\n")


file_summary.write("\n\nTo conclude, the most talked about movie on Twitter from the preceding movies is: " + top_movie_rt[0] + "\n")

if top_movie_rt[0] == "21 Jump Street":
	file_summary.write(movie_insts[0].__str__())

elif top_movie_rt[0] == "La La Land":
	file_summary.write(movie_insts[1].__str__())

elif top_movie_rt[0] == "A Dog's Purpose":
	file_summary.write(movie_insts[2].__str__())

elif top_movie_rt[0] == "Zootopia":
	file_summary.write(movie_insts[3].__str__())

file_summary.write("\n")

file_summary.close()




### IMPORTANT: MAKE SURE TO CLOSE YOUR DATABASE CONNECTION AT THE END OF THE FILE HERE SO YOU DO NOT LOCK YOUR DATABASE (it's fixable, but it's a pain). ###
conn.close()


# Write your test cases here.
print ("\n\n BELOW THIS LINE IS OUTPUT FROM TESTS:\n")

class TestCases(unittest.TestCase):

	def test_movie_cache(self):
		name ="SI206_finalproject_cache.json"
		f = open(name, 'r')
		self.assertTrue("OMDb_LaLaLand" in f.read())
		f.close()

	def test_tweet_cache(self):
		name ="SI206_finalproject_cache.json"
		f = open(name, 'r')
		self.assertTrue("21 Jump Street" in f.read())
		f.close()

	def test_get_user_tweets(self):
		result = get_twitter_info("#21jumpstreet")
		self.assertEqual(type(result), type(['eieio', 2]))

	def test_get_user_tweets_1(self):
		l = get_twitter_info("#21jumpstreet")
		self.assertEqual(type(l[1]), type({}))

	def test_movie_title(self):
		movie = get_movie_info("21jumpstreet")
		m = Movie(movie)
		self.assertEqual(m.title,"21jumpstreet")

	def test_get_actors(self):
		movie = get_movie_info("Zootopia")
		m = Movie(movie)
		self.assertEqual(type(m.get_actor_names()), type('eieio'))

	def test_movies(self):
		self.assertEqual(len(movies), 4)

	def test_str(self):
		movie = get_movie_info("A Dog's Purpose")
		m = Movie(movie)
		self.assertIn(str(m.title), m.__str__())

	def test_tweet_class(self):
		self.assertIn(twitter_instance[0].associated_movie, ["21 Jump Street", "La La Land", "A Dog's Purpose", "Zootopia"])

	def test_tweet_table_method(self):
		self.assertIn(twitter_instance[0].text, twitter_instance[0].create_twitter_table())

	def test_user_table_method(self):
		self.assertIn(twitter_instance[0].userid, twitter_instace[0].create_users_table())

	def test_get_movie_table_method(self):
		movie = get_movie_data("21 Jump Street")
		m = Movie(movie)
		self.assertIn("Jonah Hill", m.get_movie_table())





## Remember to invoke all your tests...

if __name__ == "__main__":
	unittest.main(verbosity=2)

