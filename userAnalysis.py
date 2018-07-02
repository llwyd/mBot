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
#   markovMagpie user analysis
#      v0.2
#
#
#

if os.path.isfile("users.pkl"):
    print("Loading tweet database...")
    with open("users.pkl", "rb") as fp:
        users = pickle.load(fp)
else:
    print("Database not found, quitting...")
    sys.exit()
try:
    # Initialise Tweepy
    tweetStuff = tw.tweepy_init()
    api = tw.get_api(tweetStuff) 
    #Get descriptions
    desc=[]
    for i in tqdm(range(len(users))):
    	desc.append(api.get_user(users[i]).description)
except Exception:
    traceback.print_exc()
    sys.exit(1)