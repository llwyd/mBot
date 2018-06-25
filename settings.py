import json
import re


def get_tweet_frequency():
    return int(__config["tweets"]["frequencySeconds"])


def get_tweet_history_limit():
    return int(__config["tweets"]["historyLimit"])


def get_tweet_post():
    return __config["tweets"]["post"]


def get_filter_links():
    return __config["filter"]["filterLinks"]


def get_filter_patterns():
    return __filter_patterns


def get_filter_prefixes():
    return __config["filter"]["filterPrefixes"]


def get_filter_first_words():
    return __config["filter"]["filterFirstWords"]


def get_filter_punc():
    return __config["filter"]["punctuation"]


def get_filter_min_length():
    return int(__config["filter"]["minLength"])


def is_text_to_speech_enabled():
    return __config["textToSpeech"]["enabled"]


def get_text_to_speech_rate():
    return int(__config["textToSpeech"]["rate"])


def get_config():
    return __config


with open('settings.json') as data_file:
    __config = json.load(data_file)

__filter_patterns = []

for p in __config["filter"]["filterPatterns"]:
    __filter_patterns.append(re.compile(p))
