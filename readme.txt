Samii Stoloff Final Project

PREFACE:

I apoligize that my code doesn't run.  I really tried to get it to run but in the process of trying to debug everything got fairly confusing and I am losing my mind.  This class was absolutely one of the most challenging classes I've ever taken and I don't know how I survived honestly.  In fact, I don't think I did.  Best of luck and I truly understand if I get at best a 50% on this project.  I have no conidence in myself.  

I chose option 2, using Twitter and OMdb

This code should take my input of a movie title and return the information about the movie (actos, rating, director, year, etc.).  It then searches twitter with a hashtag of the movie title to find the most retweeted and favorited tweets about the movie.  You can use this to compare the popularity of movies amongst twitter users. 

This code creates an output of different statistics of the movies including tweets for each movie with over 25 retweets and then which movie title has the most retweets amongst Twitter users.  

It creates a data base of Tweets, Users, and Movies.

You run this code by inputting your twitter information in a separate file called "twitter_info.py" with each requirement for authorization (API keys).  

In order to run this code you need:
- 206_data_access.py (python code)
- twitter_info.py (see above)

Files created:
- stoloff_final.db
- 206_final_cache.json
- file_summary.txt

To run you must install:
- requests
- tweepy
- sqlite3
- regular expressions (re)


Functions:

def get_twitter_info (line 57)
- input is required
- returns tweets from twitter or from a cache if the information is already in the cache

def get_movie_info (line 78)
- input is required
- returns a dictionary of movie information, from OMdb

def get_actor_names (line 141)
- no input
- returns the names of actors that are in a movie

def create_movie_table (line 145)
- no input
- returns the movie table, which includes the movie id, title, director, rating, and the leading actor.

def create_twitter_tabe (line 183)
- no input
- returns a table of twitter infomation including user ID, tweet text, the movie that is associated with the tweet, the number of retweets and the number of favorites.

def create users_table (line 189)
- no input
- returns a table of twitter users which includes the user ID, user name, and the number of favorites the user has made.

Classes:

class Movie (line 132)
- one instance of class Movie represents a single movie
- required is a movie dictionary with all of the OMdb information
- Methods: 
    - def get_actor_names (line 141)
      - no input
      - returns the names of actors that are in a movie

    - def create_movie_table (line 145)
      - no input
      - returns the movie table, which includes the movie id, title, director, rating, and the leading actor.

class Search_Twitter (line 170)
- one instance of class Search_Twitter represents the information aquired from a single tweet about a movie
- required is a movie and tweet 
- Methods:
    - def create_twitter_tabe (line 183)
      - no input
      - returns a table of twitter infomation including user ID, tweet text, the movie that is associated with the tweet, the number of retweets and the number of favorites.

    - def create users_table (line 189)
      - no input
      - returns a table of twitter users which includes the user ID, user name, and the number of favorites the user has made.


Database:

Movie Table:
- each row represents a single movie
- each row contains the movie_id, movie title, leading actor, director, year, and rating

Tweet Table: 
- each row represents a single tweet
- each row contains the tweet id, the user name of the tweeter, tweet retweet number, tweet favofrite number, tweet text, and the associated movie

User Table:
- each row represents a single Twitter user
- each row contains a user id, user name, and number of favorites


I chose to do this project because we did a ton of homeworks on twitter caching and searching so it was the most confortable to work with.