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

Authentication information should be in a twitter_info file...
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


movie_titles = ["21 Jump Street", "La La Land", "A Dog's Purpose", "Zootopia"]

movie_dictionary = []
for title in movie_titles: 
	movies_dictionary.append(get_movie_info(movie))

movie_instance = []
for movie in movies_dictionary:
	movie_instance.append(Movie(movie))


for i in movie_instance:
	cur.execute(statement_1, m.create_movie_table())

class Search_Twitter():
	def __init__(self, tweet, movie):
		self.tweet = tweet
		self.id = tweet['id_str']
		self.userid = tweet['user']['id_str']
		self.text = tweet['text']
		self.retweets = tweet['retweet_count']
		self.screen_name = tweet['user']['screen_name']
		self.associated_movie = movie
		self.favorites = tweet['favorite_count']
		self.user_favorites = tweet["user"]["favourites_count"]


	def create_twitter_table(self):

		table_1 = self.id, self.userid, self.text, self.associated_movie, self.retweets, self.favorites

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
file_summary.write("Samii Stoloff\n")
file_summary.write("SI 206 Final Project Summary\n\n")
file_summary.write("I used data analytics on four different movies to see what was being said on Twitter about them.  This project summary will allow you to compare the different movies based on a variety of statistics. \n\nThe movies I chose to compary were 21 Jump Street, La La Land, A Dog's Purpose, and Zootopia. Each movie was searched on Twitter with their respective hashtags")


statement = 'SELECT * FROM Tweets WHERE num_retweets > 25'
result = cur.execute(statement)
twitter_rt = []
for rt in result.fetchall():
	twitter_rt.append(rt)


sorted_twitter_rt = sorted(twitter_rt key = lambda x: x[4], reverse = True)

most_rt_tweets = sorted_tweets_for_rts[:5]

most_rt_tweets_str = " Here are the five most popular tweets about each movie.  Popular tweets have the most retweets on twitter.\n" 

file_summary.write(most_popular_tweets_str)
for i in range(len(most_popular_tweets)):
	file_summary.write("\n")
	file_summary.write(str(i+1) + ". Tweet Text: " +str(most_popular_tweets[i][1]))
	file_summary.write( "\nAssociated Movie: " + str(most_popular_tweets[i][3]))
	file_summary.write( "\nTweet Id: "+ str(most_popular_tweets[i][0]))
	file_summary.write( "\nUser Id: "+ str(most_popular_tweets[i][2]))
	file_summary.write( "\nNumber of Retweets: " + str(most_popular_tweets[i][4]))
	file_summary.write("\n")



# Make an inner join query statement to find the screen name, associated movie, user favorites and their number of retweets on their tweet from the inner join of Tweets and Users tables where the number of rewtweets and user favorites are both greater than 50, then save that resulting list of tuples in a dictionary named variable most_popular_movies_tweeters
# Make sure you do this using dictonary comprehension
statement = 'SELECT screen_name, associated_movie, user_favorites, num_retweets FROM Tweets INNER JOIN Users ON Tweets.user_id=Users.user_id WHERE num_retweets >50 AND user_favorites > 50'
result = cur.execute(statement)
#most_popular_movies_tweeters = {r[1]:(r[0],r[2],r[3]) for r in result.fetchall()}
most_popular_movies_tweeters = {r[0]:(r[1],r[2],r[3]) for r in result.fetchall()}
# sorted_most_popular_movies_tweeters = sorted(most_popular_movies_tweeters, key = lambda x: most_popular_movies_tweeters[x][0])
# print (sorted_most_popular_movies_tweeters)
# for r in result.fetchall():
# 	most_popular_movies_tweeters.append(r)
# print (most_popular_movies_tweeters)
# print ('**************')

tweeters_str = "\nWhen looking at users who tweeted about certain movies, I looked at what popular users (people who had over 50 user favorites and 50 retweets on their tweet) and what movie they tweeted about. It becomes evident that certain movies attract more attention than others:\n"
file_summary.write(tweeters_str)
#file_summary.write("The statistics after the username are as follows: (Movie tweeted about, number of user favorites, number of retweets)\n")
for key in most_popular_movies_tweeters.keys():
	file_summary.write("\n")
	file_summary.write("User: " + key + "\n Associated Movie: " +str(most_popular_movies_tweeters[key][0]) + "\n User Favorites: " + str(most_popular_movies_tweeters[key][1]) + "\n Number of Tweet Retweets: " + str(most_popular_movies_tweeters[key][2]))
	file_summary.write("\n")

#for key in most_popular_movies_tweeters.keys():

#Ecount = collections.Counter(most_popular_movies_tweeters[most_popular_movies_tweeters.keys()][0])
counted_movies = [most_popular_movies_tweeters[key][0] for key in most_popular_movies_tweeters.keys()]
print (counted_movies)
count =collections.Counter(counted_movies).most_common()
print (count[0])
file_summary.write("\n After looking at the most popular tweets about these movies, I wanted to see out of these movies, which one was tweeted about the most (out of the popular tweets)")
file_summary.write("\n" + count[0][0] + " had the most popular tweets with " + str(count[0][1]) + " tweets."  )


# Use dictionary accumulation in order to calculate the total number of retweets each of the associated movies have had. 
# Each key should be the associated movie and each value should add all of the retweets together. 
movie_retweets = {}
for tweet in tweets_for_rts:
	if tweet[3] not in movie_retweets:
		movie_retweets[tweet[3]] = tweet[4]
	else:
		movie_retweets[tweet[3]] += tweet[4]
file_summary.write("\n\nWhen looking at each movie, here are the total number of retweets on the tweets pulled associated to each movie:\n")
for movie in movie_retweets.keys():
	file_summary.write(movie + " Retweets:  " + str(movie_retweets[movie]))
	file_summary.write("\n")
# print (movie_retweets)

# Then sort a list of the dictionary keys based on the number of total number of retweets for each movie, and store the top movie and its number of retweets in a varaiable called top_movie_retweets.
sorted_movie_retweets = sorted(movie_retweets, key = lambda x: movie_retweets[x], reverse = True)
#print (sorted_movie_retweets)
top_movie_retweets = [sorted_movie_retweets[0], movie_retweets[sorted_movie_retweets[0]]]
file_summary.write("\nThe most tweeted about movie: " +str(top_movie_retweets[0]) + " with " +str(top_movie_retweets[1]) + " retweets!\n")
# print (top_movie_retweets)


# Pull the movie title, rating, and box office performance for each movie with a query statment. Save this information in a list named movie_performances.
# Save this information by using list comprehension
statement = 'SELECT title, rating, box_office FROM Movies'
result = cur.execute(statement)
movie_performances = [r for r in result.fetchall()]
sorted_movie_performances = sorted(movie_performances, key = lambda x: x[1], reverse = True)
file_summary.write("\nHere were the performances of each of the three movies (listed by their ratings), found from the IMDb database:\n\n")
for movie in sorted_movie_performances:
	file_summary.write(movie[0] + ": Rating: " + str(movie[1]) + " Box Office Performance: " + str(movie[2]))
	file_summary.write("\n")
#print (movie_performances)


statement = 'SELECT top_actor FROM Movies'
result = cur.execute(statement)
movie_actors = {r[0] for r in result.fetchall()}

file_summary.write("\nFrom these movies, the main actors were:\n")
for actor in movie_actors:
	file_summary.write(actor)
	file_summary.write("\n")
# print (movie_actors)


file_summary.write("\n\nFrom all this data, the movie I would recommend you see is: " + top_movie_retweets[0] + "\n")
if top_movie_retweets[0] == "Beauty and the Beast":
	file_summary.write(movie_insts[0].__str__())
elif top_movie_retweets[0] == "The Boss Baby":
	file_summary.write(movie_insts[1].__str__())
elif top_movie_retweets[0] == "Logan":
	file_summary.write(movie_insts[2].__str__())

file_summary.write("\n\n\n\n")

file_summary.close()




### IMPORTANT: MAKE SURE TO CLOSE YOUR DATABASE CONNECTION AT THE END OF THE FILE HERE SO YOU DO NOT LOCK YOUR DATABASE (it's fixable, but it's a pain). ###
conn.close()



# Put your tests here, with any edits you now need from when you turned them in with your project plan.
# Write your test cases here.
print ("\n\n BELOW THIS LINE IS OUTPUT FROM TESTS:\n")

class Task1(unittest.TestCase):
	def test_tweet_caching(self):
		name ="SI206_finalproject_cache.json"
		f = open(name, 'r')
		self.assertTrue("Beauty and the Beast" in f.read())
		f.close()
	def test_movie_caching(self):
		name ="SI206_finalproject_cache.json"
		f = open(name, 'r')
		self.assertTrue("OMDb_Logan" in f.read())
		f.close()
	def test_get_user_tweets(self):
		res = get_twitter_data("#Logan")
		self.assertEqual(type(res), type(['hi', 5]))
	def test_movie_title(self):
		mov = get_movie_data("Logan")
		i = Movie(mov)
		self.assertEqual(i.title,"Logan")
	def test_get_actors(self):
		mov = get_movie_data("Logan")
		i = Movie(mov)
		self.assertEqual(type(i.get_actors()), type('hello'))
	def test_movies3(self):
		self.assertEqual(len(movies), 3)
	def test_get_user2(self):
		l = get_twitter_data("#beautyandthebeast")
		self.assertEqual(type(l[1]), type({}))
	def test_str(self):
		mov = get_movie_data("Logan")
		i = Movie(mov)
		self.assertIn(str(i.title), i.__str__())
	def test_tweet_table_method(self):
		self.assertIn(twitter_insts[0].text, twitter_insts[0].get_twitter_table())
	def test_tweet_class(self):
		self.assertIn(twitter_insts[0].associated_movie, ['Beauty and the Beast', "Logan", 'The Boss Baby'])
	def test_user_table_method(self):
		self.assertIn(twitter_insts[0].userid, twitter_insts[0].get_users_table())
	def test_get_movie_table_method(self):
		mov = get_movie_data("Beauty and the Beast")
		i = Movie(mov)
		self.assertIn("Bill Condon", i.get_movie_table())






## Remember to invoke all your tests...

if __name__ == "__main__":
	unittest.main(verbosity=2)



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