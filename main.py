#Write crawler code

import sys
import tweepy
from auth import TwitterAuth

auth = tweepy.OAuthHandler(TwitterAuth.consumer_key, TwitterAuth.consumer_secret)
auth.set_access_token(TwitterAuth.access_token, TwitterAuth.access_token_secret)

api = tweepy.API(auth)

query = raw_input("What tag do you want to collect?")
count = 1

for tweet in tweepy.Cursor(api.search,q=query,count=100,\
                           lang="en",\
                           since_id=2015-06-1).items():
    	print count
	print tweet.created_at, tweet.text
	count += 1

    





