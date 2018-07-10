import collections
import datetime as dt
import json
import os
import pickle
import random as r
import re
import sys

import tweepy
import traceback
import settings
import twitter as tw
from collections import Counter
from tqdm import tqdm
#
#
#
#   markovMagpie
#      v0.2
#
#	Pure Data Harvesting
#
#
try:
    # Initialise Tweepy
    tweetStuff = tw.tweepy_init()
    api = tw.get_api(tweetStuff)

    # Set Parameters
    # number of tweets to read (capped at 200 by twitter)
    numTweet = settings.get_tweet_history_limit()
    # time between tweets in seconds
    delay = settings.get_tweet_frequency()
    # size of overall storage buffer
    buffSize = 1000
    # current position of buffer
    buffPos = 0
    # master list of tweets
    master = []
    # s=[]
    # key, array of first values
    e = []
    t = []
    # define dictionary, this will hold each word and the location
    d = {}
    d0 = {}
    # Filter for removing punctuation (except sentence endings)
    puncFilter = str.maketrans('', '', '…\"$%&\'()“”"*+-/<=>[\\]^_`{|}~')
    # flag for enabling tweets
    active = settings.get_tweet_post()
    # flag for enabling punctuation filter
    punc = settings.get_filter_punc()

except Exception:
    traceback.print_exc()
    sys.exit(1)

rateLimit = False

try:
    if os.path.isfile("misc.json"):
        with open('misc.json') as data_file:
            pos = json.load(data_file)
    else:
        pos = {'id': 0}
    # get tweets
    if pos['id'] == 0:
        print("pos=0")
        tweets = api.home_timeline(count=numTweet, tweet_mode='extended')
    else:
        print("pos!=0")
        tweets = api.home_timeline(count=numTweet, tweet_mode='extended', since_id=pos['id'])

    pos['id']=tweets.max_id
    with open('misc.json','w') as data_file:
        json.dump(pos,data_file)    

    # filter text and sort by ids
    latestTweets = {}
    for x in tweets:
        latestTweets[x.id] = x.full_text

    # re-sort the tweets such that the newest appears first in the dict
    latestTweets = collections.OrderedDict(sorted(latestTweets.items(), reverse=True))

    # Put current keys into callable list
    keys = list(latestTweets.keys())

	#Harvest profile info
    if os.path.isfile("users.pkl"):
        print("Loading user database...")
        with open("users.pkl", "rb") as fp:
            users = pickle.load(fp)
    else:
        print("User database not found, creating new...")
        users = []
    for i in range(len(tweets)):
        users.append(tweets[i].user.id);

    print("Storing database...")
    with open("users.pkl", "wb") as fp:
        pickle.dump(users, fp)


    # begin filtering

    # collect list to purge
    purgeList = []

    for i in range(len(keys)):
        # Filter Retweets
        if latestTweets[keys[i]][0:2] == "RT":
            purgeList.append(i)

        # Filter direct Messages
        elif latestTweets[keys[i]][0] == '@':
            purgeList.append(i)

    # purge list
    for i in range(len(purgeList)):
        latestTweets.pop(keys[purgeList[i]])
    keys = list(latestTweets.keys())

    # Master list of tweets
    new = list(latestTweets.values())
except:
    rateLimit = True
    print("Rate limit exceeded, proceeding anyway")

if os.path.isfile("database.pkl"):
    print("Loading tweet database...")
    with open("database.pkl", "rb") as fp:
        s = pickle.load(fp)
else:
    print("Database not found, creating new...")
    s = []
if not rateLimit:
    for i in range(len(new)):
        s.append(new[i])

# Remove textless image only tweets;
purgeList = []
for i in tqdm(range(len(s))):
    if s[i][0:5] == "https":
        purgeList.append(i)
for i in range(len(purgeList) - 1, -1, -1):
    s.pop(purgeList[i])

# punctuation filter
if punc:
    print("Punctuation Filtering...")
    for i in range(len(s)):
        s[i] = s[i].translate(puncFilter)

# Replace &
for i in range(len(s)):
    s[i] = s[i].replace("amp;", "and")

print("Storing database...")
with open("database.pkl", "wb") as fp:
    pickle.dump(s, fp)

print("Tweet database entries: " + str(len(s)) + " tweets")
dataSize = os.stat('database.pkl').st_size
print("Database size: " + str(dataSize) + "Bytes")