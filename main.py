#Write crawler code

import sys
import re
import tweepy
from auth import TwitterAuth
import json
from nltk.tokenize import word_tokenize

auth = tweepy.OAuthHandler(TwitterAuth.consumer_key, TwitterAuth.consumer_secret)
auth.set_access_token(TwitterAuth.access_token, TwitterAuth.access_token_secret)

api = tweepy.API(auth)

filename = 'data.json'

@classmethod
def parse(cls, api, raw):
    tweet = cls.first_parse(api, raw)
    setattr(tweet, 'json', json.dumps(raw))
    return tweet
 
# Status() is the data model for a tweet
tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse

def scraping_tweets(query):
	
	count = 1

	tweets = tweepy.Cursor(api.search,q=query,count=10,\
		                   lang="en",\
		                   since_id=2015-06-01).items()
	for tweet in tweets:
	    	print count
		user_id = tweet.from_user_id
		user = api.get_user(user_id)
		print "user: %s, user id: %s, screen_name: %s, created_at: %s, text: %s." % (tweet.from_user, tweet.from_user_id, user.screen_name, tweet.created_at, tweet.text)
		count += 1
	
def dump(data):
    with open(filename, 'w') as outfile:
    	json.dump(data.json, outfile)

def store_data(data):
	try:
		with open(filename, 'a') as f:
			f.write(data)
			return True
	except BaseException as e:
		    print("Error on_data: %s" % str(e))
	return True
 
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

def process_tweets():
	with open(filename, 'r') as f:
	    for line in f:
		tweet = json.loads(line)
		tokens = preprocess(tweet['text'])
		do_something_else(tokens)

# Scraping starts here!   
query = raw_input("What tag do you want to collect?")

tweets = scraping_tweets(query)
for tweet in tweets:
	dump(tweet)




