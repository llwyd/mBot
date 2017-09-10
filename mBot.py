#
#   Markov chain bot
#
#
#
import tweepy
import random as r
import time
import re
import tweet_store
from tqdm import tqdm
import settings
import numpy as np
import os

#-------------------------------------------------------------
#
#       VARIOUS FUNCTIONS
#
#-------------------------------------------------------------

# ----------------------------
#   Text Filtering
# ----------------------------
# Filter tweets with particular keywords
def filter_word(t, keyword):
    for i in range(len(t)):
        for j in range(len(t[i])):
            if t[i][j] == keyword:
                return True
    return False


# Filter tweets with mentions and hashtags
def filter_prefix(t, prefix):
    for i in range(len(t)):
        for j in range(len(t[i])):
            if t[i][j][0] == prefix:
                return True
    return False


# ----------------------------
#   text-to-speech
# ----------------------------
def init_tts():
    if settings.is_text_to_speech_enabled():
        speak = pyttsx3.init()
        speak.setProperty('rate', settings.get_text_to_speech_rate())
        return speak
    return None


def say(text):
    if settings.is_text_to_speech_enabled():
        speak.say(text)
        speak.runAndWait()


# ----------------------------
#   Tweepy stuff
# ----------------------------
def get_api(info):
    auth = tweepy.OAuthHandler(info['ck'], info['cs'])
    auth.set_access_token(info['at'], info['ats'])
    return tweepy.API(auth)


def post_tweet(statusmsg, info):
    auth = tweepy.OAuthHandler(info['ck'], info['cs'])
    auth.set_access_token(info['at'], info['ats'])

    try:
        api.update_status(status=statusmsg)
        print('Tweet Successful')
    except Exception:
        # Stops everything crashing if there is a connection issue.
        print('Tweet Unsuccessful')


# get tweets as a map of <id, message>
def get_tweets(num):
    if tweet_store.num() is 0:
        tweets = api.home_timeline(count=num)
    else:
        tweets = api.home_timeline(count=num, since_id=list(tweet_store.tweets.keys())[0])

    tweet_store.save(tweets, num)

    count = 0

    for tid in tqdm(list(tweet_store.tweets.keys()), desc='Retrieving Timeline'):

        text = tweet_store.get(tid)

        if filter_tweet(tid, text):
            continue

        # only grab the full tweet if we need it
        # as this is slow
        if '…' in text:
            tweet_store.update(tid, get_full_tweet(tid))
            if filter_tweet(tid, text):
                continue

        if settings.get_filter_links():
            tweet_store.update(tid, " ".join(list(filter(lambda o: not re.compile(r'.*(https|http)://').search(o), tweet_store.get(tid).split()))))

        count += 1
        # print(text)

    return tweet_store.tweets


def filter_tweet(tid, text):

    # if matches any patterns
    for filterPattern in settings.get_filter_patterns():
        if filterPattern.search(text):
            tweet_store.remove(tid)
            return True

    # or matches any prefixes
    split = text.split()

    for filterPrefix in settings.get_filter_prefixes():
        if filter_prefix(split, filterPrefix):
            tweet_store.remove(tid)
            return True

    # or matches any first words
    for filterFirstWord in settings.get_filter_first_words():
        if split[0] == filterFirstWord:
            tweet_store.remove(tid)
            return True

    # or is too short
    if len(split) < settings.get_filter_min_length():
        tweet_store.remove(tid)
        return True

    return False


def get_full_tweet(tweet_id):
    return api.get_status(tweet_id, tweet_mode='extended')._json['full_text']


def tweepy_init():
    print("Initialising Tweepy...")
    tokens = open('tokens.txt')
    info = {
        'ck': tokens.readline()[:-1],
        'cs': tokens.readline()[:-1],
        'at': tokens.readline()[:-1],
        'ats': tokens.readline()[:-1]
    }

    tokens.close()
    print("Complete!")
    return info

def build_word(e,d,d0):
    pf0 = ""
    # print("Building output...", end="", flush=True)
    rFlag = True  # flag to check for repeat
    while rFlag:
        f0 = e[r.randint(0, len(e) - 1)]  # first word
        if f0 != pf0 and len(d[f0]) > 0:
            rFlag = False
    pf0 = f0  # Store first word into variable so it can avoid repeats
    f1 = d[f0][r.randint(0, len(d[f0]) - 1)]  # second word
    # f2 = d0[f1][r.randint(0, len(d0[f1]) - 1)]  # anything after can follow this
    output = f0 + " " + f1
    op = f1
    if len(d0[f1]) > 0:
        end = False
        while not end:
            try:
                on = d0[op][r.randint(0, len(d0[op]) - 1)]  # output new
                op = on  # output previous
                output = output + " " + op
                if len(d0[op]) == 0:
                    # output=output + "."
                    end = True
            except:
                # output=output + "."
                break

    # Add a full stop to the end if necessary.
    lastchar = output[len(output) - 1]
    if lastchar != '.' or lastchar != '?' or lastchar != '!':
        output += "."

    # print("Complete!\n", flush=True)

    return output

#-------------------------------------------------------------
#
#       PROGRAM BEGINS HERE
#
#-------------------------------------------------------------
tweepyInfo = tweepy_init()
api = get_api(tweepyInfo)

# ----------------------------
# Parameters
# ----------------------------
# number of tweets to read (capped at 200 by twitter)
numTweet = settings.get_tweet_history_limit()
# time between tweets in seconds
delay = settings.get_tweet_frequency()
# size of overall storage buffer
buffSize = 1000
# current position of buffer
buffPos = 0
#master list of tweets
master = []
# key, array of first values
e = []
t = []
# define dictionary, this will hold each word and the location
d = {}
d0 = {}
# Filter for removing punctuation (except sentence endings)
puncFilter = str.maketrans('', '', '\"$%&\'()*+,-/:;<=>@[\\]‘^_`{|}~')
#flag for enabling tweets
active=settings.get_tweet_post();

print("-----------------------------------------", flush=True)
# get latest tweets
s = list(get_tweets(numTweet).values())
# filter punctuation
for i in range(len(s)):
    s[i] = s[i].translate(puncFilter)
#check if firstWords database exists
if(os.path.isfile("firstWords.npy")==True):
    #load the database
    e=numpy.load("firstWords.npy");
    #typecase to list for consistency
    e=list(e);
else:
    #if not then create empty list
    e=[];
#--------------------------------------
#   begin filtering of firstWords
#--------------------------------------
for i in range(len(s)):
    if s[i] is None:
        continue
    dup=False
    for j in range(len(e)):
        if(e[j]==s[i].split()[0]):
            dup=True;
            break;
    if(dup!=True):
        e.append(s[i].split()[0]);
    # array of separated words for latest tweets
    t.append(s[i].split());

#--------------------------------------
#   begin filtering of secondWords
#--------------------------------------
#check if database exists
if(os.path.isfile("secondWords.npy")==True):
    #load the database
    d=numpy.load("secondWords.npy").item();
else:
    #if not then create empty dictionary
    d={};
#check if the first word already exists in the dictionary
for i in range(len(e)):
    if((e[i] in d))==False:
        d[e[i]]=[];
#Create dictionary of first words and second words
for i in range(len(s)):
    if s[i] is None:
        continue
    dup=False
    for j in range(len(d[t[i][0]])):
        if(d[t[i][0]][j])==t[i][1]:
            dup=True;
            break;
    if(dup!=True):
        d[t[i][0]].append(t[i][1]);

#--------------------------------------
#   begin filtering of otherWords
#--------------------------------------
#check if database exists
if(os.path.isfile("otherWords.npy")==True):
    #load the database
    d0=numpy.load("otherWords.npy").item();
else:
    #if not then create empty dictionary
    d0={};
#check if word already exists
for i in range(len(s)):
    if s[i] is None:
        continue
    for p in range(1,len(t[i])):
        if not (t[i][p] in d0.keys()):
            d0[t[i][p]] = [];
#add new words to database
for i in range(len(s)):
    if s[i] is None:
        continue
    for j in range(2,len(t[i])):
        dup=False
        for k in range(len(d0[t[i][j-1]])):
            if d0[t[i][j-1]][k]==t[i][j]:
                dup=True;
                break;
        if(dup!=True):
            d0[t[i][j-1]].append(t[i][j]);
 

output = build_word(e,d,d0)
while len(output) > 140:
    output = build_word(e,d,d0)

print("*****************************************", flush=True)
print("" + output + "", flush=True)
print("*****************************************", flush=True)

if(active==True):
    post_tweet(output, tweepyInfo)