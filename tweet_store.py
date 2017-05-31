import collections

# saved tweets
tweets = {}


def save(new_tweets, threshold):

    global tweets

    for new_tweet in new_tweets:
        tweets[new_tweet.id] = new_tweet.text

    tweets = collections.OrderedDict(sorted(tweets.items(), reverse=True))

    if num() >= threshold:
        tweets = collections.OrderedDict(e for i, e in enumerate(tweets.items()) if 0 <= i <= threshold-1)


def get_range(d, begin, end):
    return


def get(tid):
    return tweets[tid]


def update(tid, text):
    tweets[tid] = text
    return text


def remove(tid):
    tweets.pop(tid)


def num():
    return len(tweets)
