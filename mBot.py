#
#   Markov chain bot
#
#
#
import tweepy
import collections
import random as r
import string
import time
import tweet_store
from tqdm import tqdm


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
            filter_tweet(tid, text)
        count += 1
        # print(text)

    return tweet_store.tweets


def filter_tweet(tid, text):

    split = text.split()
    is_filtered = filter_prefix(split, '&') \
        or filter_prefix(split, '@') \
        or len(split) <= 2 \
        or split[0] == "RT" \
        or split[0] == "@"

    if is_filtered:
        tweet_store.remove(tid)

    return is_filtered


def get_full_tweet(tweet_id):
    return api.get_status(tweet_id, tweet_mode='extended')._json['full_text']


def tweepy_init():
    print("Initialising Tweepy...")
    tokens = open('tokens.txt')
    info = {
        'ck': "",
        'cs': "",
        'at': "",
        'ats': ""
    }

    consumer_key = tokens.readline()
    consumer_secret = tokens.readline()
    access_token = tokens.readline()
    access_token_secret = tokens.readline()
    tokens.close()

    # Remove the NewLineCharacter;
    info['ck'] = consumer_key[:-1]
    info['cs'] = consumer_secret[:-1]
    info['at'] = access_token[:-1]
    info['ats'] = access_token_secret[:-1]
    print("Complete!")
    return info


# ----------------------------
#   Markov Stuff
# ----------------------------
def first_word(s):
    e = []
    t = []
    for i in range(len(s)):
        if s[i] is None:
            continue
        splitText = s[i].split()
        if splitText[-1][0:5] == "https":
            t.append(splitText[:-1])
        else:
            t.append(splitText)
        e.append(t[i][0])
    return e, t


# this loop works out which words are duplicate so it can begin the p structure
def second_word(s, e, t):
    d = {}
    for i in range(len(s)):
        if s[i] is None:
            continue
        d[e[i]] = []
        for j, k in enumerate(e):
            if k == e[i] and len(t[j]) > 1:
                d[e[i]].append(t[j][1])
    return d


def other_word(s, e, t):
    d0 = {}
    for i in range(len(s)):
        if s[i] is None:
            continue
        for p in range(len(t[i])):
            d0[t[i][p]] = []
            for j, k in enumerate(t[i]):
                if k == t[i][p] and j != len(t[i]) - 1:
                    d0[t[i][p]].append(t[i][j + 1])
    return d0


tweepyInfo = tweepy_init()
api = get_api(tweepyInfo)

# Parameters

# number of tweets to read (capped at 200 by twitter)
numTweet = 200
# size of overall storage buffer
buffSize = 1000
# current position of buffer
buffPos = 0

master = [None] * buffSize
match = False

delay = 1800  # in seconds
# key, array of first values
e = []
t = []
# define dictionary, this will hold each word and the location
d = {}
d0 = {}
pf0 = ""

# Filter for removing punctuation (except sentence endings)
puncFilter = str.maketrans('', '', '\"$%&\'()*+,-/:;<=>@[\\]‘^_`{|}~')

while True:
    # try:
    print("-----------------------------------------", flush=True)
    s = list(get_tweets(numTweet).values())
    for i in range(len(s)):
        s[i] = s[i].translate(puncFilter)
        match = False

        for j in range(len(master)):
            if s[i] == master[j]:
                match = True
                break

        if not match:
            master[buffPos] = s[i]
            buffPos += 1
            buffPos %= buffSize

    time.sleep(1)
    print("Calculating markov chain...", end="", flush=True)
    e, t = first_word(master)
    d = second_word(master, e, t)
    d0 = other_word(master, e, t)
    print("Complete!", flush=True)

    print("Building output...", end="", flush=True)
    rFlag = True  # flag to check for repeat
    while rFlag:
        f0 = e[r.randint(0, len(e) - 1)]  # first word
        if f0 != pf0 and len(d[f0]) > 0:
            rFlag = False

    pf0 = f0  # Store first word into variable so it can avoid repeats
    f1 = d[f0][r.randint(0, len(d[f0]) - 1)]  # second word
    f2 = d0[f1][r.randint(0, len(d0[f1]) - 1)]  # anything after can follow this
    output = f0 + " " + f1 + " " + f2
    op = f2
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
    if output[len(output) - 1] != '.':
        output = output + "."

    print("Complete!\n", flush=True)
    print("*****************************************", flush=True)
    print("\n" + output + "\n", flush=True)
    print("*****************************************", flush=True)
    # e.clear();
    # t.clear();
    # d.clear();
    # s.clear();
    # d0.clear();
    # post_tweet(output, tweepyInfo)
    # except:
    #	print("Algorithm Error, Retrying in 5 minutes.");
    time.sleep(delay)
