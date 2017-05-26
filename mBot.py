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
#  get tweets as a map of <id, message>
def get_tweets(user, num):
    tweets = api.user_timeline(id=user, count=num)
    messages = {}
    count = 0
    for tweet in tweets:

        text = tweet._json['text']
        if '…' in text:
            text = get_full_tweet(tweet.id)

        #  we don't want 1 word tweets or retweets
        if len(text.split()) <= 1 or text.split()[0] == "RT" or text.split()[0] == "@":
            continue

        messages[tweet.id] = text
        count += 1
        print(text)

    return messages


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

tweepyInfo = tweepy_init()
api = get_api(tweepyInfo)

# f = open('data.txt')
# s = f.readlines()
# f.close()
numTweet = 100  # number of tweets to read
buffSize = 1000 # size of overall storage buffer
follow = open('follow.txt')
s = list(get_tweets(follow.readline(), numTweet).values())
follow.close()
time.sleep(1)

e = []
t = []

for i in range(len(s)):
    splitText = s[i].split()
    if splitText[-1][0:5] == "https":
        t.append(splitText[:-1])
    else:
        t.append(splitText)
    e.append(t[i][0])

# this loop works out which words are duplicate so it can begin the p structure
d = {}  # define dictionary, this will hold each word and the location
for i in range(len(s)):
    # d[e[i]]=[t[i][1]];
    d[e[i]] = []
    for j, k in enumerate(e):
        if (k == e[i]) and (len(t[j]) > 1):
            d[e[i]].append(t[j][1])

size = 10
d0 = {}
for i in range(len(s)):
    for p in range(len(t[i])):
        d0[t[i][p]] = []
        for j, k in enumerate(t[i]):
            if (k == t[i][p]) and (j != len(t[i]) - 1):
                d0[t[i][p]].append(t[i][j + 1])


delay = 5 #in seconds
while True:
	f0 = e[r.randint(0, len(s) - 1)]  # first word
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
	            # output=output+".";
	            end = True
	    except:
	        #	output=output+".";
	        break
	print("\n\n" + output)
	time.sleep(delay);
	#  post_tweet(output, tweepyInfo)
