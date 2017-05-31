import collections

# saved tweets
tweets = {}


def save(new_tweets, threshold):

    global tweets

    for new_tweet in new_tweets:
        tweets[new_tweet.id] = new_tweet.text

    tweets = collections.OrderedDict(sorted(tweets.items(), reverse=True))

    if len(tweets) >= threshold:
        tweets = tweets[:threshold - 1]


def get(tid):
    return tweets[tid]


def update(tid, text):
    tweets[tid] = text
    return text


def remove(tid):
    tweets.pop(tid)


def num():
    return len(tweets)
