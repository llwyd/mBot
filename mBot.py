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


def get_tweets(user,num):
    tweets = api.user_timeline(id=user, count=num)
    messages = []
    for tweet in tweets:

        text = get_full_tweet(tweet.id)
        t=text.split();
        #print(text)
        if len(text.split()) <= 1:
            continue
        elif t[0]=="RT":
        	continue
        messages.append(text)
        print(text)
    return messages


def get_full_tweet(id):
    return api.get_status(id, tweet_mode='extended')._json['full_text']


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
numTweet=50;#number of tweets to read
follow = open('follow.txt')
s = get_tweets(follow.readline(),numTweet)
follow.close()
time.sleep(1)

e = []
t = []
splitText=[]
for i in range(len(s)):
	splitText=s[i].split();
	if(splitText[-1][0:5]=="https"):
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
        if k == e[i]:
            d[e[i]].append(t[j][1])

size = 10
d0 = {}
for i in range(len(s)):
    for p in range(len(t[i])):
        d0[t[i][p]] = []
        for j, k in enumerate(t[i]):
            if (k == t[i][p]) and (j != len(t[i]) - 1):
                d0[t[i][p]].append(t[i][j + 1])

f0 = e[r.randint(0, len(s) - 1)]  # first word
f1 = d[f0][r.randint(0, len(d[f0]) - 1)]  # second word
f2 = d0[f1][r.randint(0, len(d0[f1]) - 1)]  # anything after can follow this
output = f0 + " " + f1 + " " + f2
op = f2
outLen = r.randint(5, 10)

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
#post_tweet(output, tweepyInfo)
