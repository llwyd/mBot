import re

import tweepy
from tqdm import tqdm

import settings
import tweet_store


def tweepy_init():
    tokens = open('tokens.txt')
    info = {
        'ck': tokens.readline()[:-1],
        'cs': tokens.readline()[:-1],
        'at': tokens.readline()[:-1],
        'ats': tokens.readline()[:-1]
    }

    tokens.close()
    return info


def get_api(info):
    """ Get twitter api handle with auth """
    auth = tweepy.OAuthHandler(info['ck'], info['cs'])
    auth.set_access_token(info['at'], info['ats'])
    return tweepy.API(auth)


def get_tweets(num, api):
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
            tweet_store.update(tid, get_full_tweet(tid, api))
            if filter_tweet(tid, text):
                continue

        if settings.get_filter_links():
            tweet_store.update(tid, " ".join(
                list(filter(lambda o: not re.compile(r'.*(https|http)://').search(o), tweet_store.get(tid).split()))))

        count += 1

    return tweet_store.tweets


# Filter tweets with mentions and hashtags
def filter_prefix(t, prefix):
    for i in range(len(t)):
        for j in range(len(t[i])):
            if t[i][j][0] == prefix:
                return True
    return False


def filter_tweet(tid, text):
    """ Indicates whether a tweet should be filtered out """

    # too short
    split = text.split()
    if len(split) < settings.get_filter_min_length():
        tweet_store.remove(tid)
        return True

    # matches any patterns
    for filterPattern in settings.get_filter_patterns():
        if filterPattern.search(text):
            tweet_store.remove(tid)
            return True

    # or matches any prefixes
    for filterPrefix in settings.get_filter_prefixes():
        if filter_prefix(split, filterPrefix):
            tweet_store.remove(tid)
            return True

    # or matches any first words
    for filterFirstWord in settings.get_filter_first_words():
        if split[0] == filterFirstWord:
            tweet_store.remove(tid)
            return True

    return False


def get_full_tweet(tweet_id, api):
    return api.get_status(tweet_id, tweet_mode='extended')._json['full_text']
