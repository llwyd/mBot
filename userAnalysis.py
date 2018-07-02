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
import matplotlib.pyplot as plt
import numpy as np
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
    count={}
    users.sort();
    for i in range(len(users)):
        count[users[i]]=users.count(users[i])
    del users
    users=list(count.keys());
    users.sort();
    

    with open('dataAnalysis.json','r') as f:
        k=json.load(f);
    keyWords=k['keywords'];
    regex=[]
    for i in range(len(keyWords)):
    	regex.append(re.compile(keyWords[i]))
    tweetCount={}
    for i in range(len(keyWords)):
    	tweetCount[keyWords[i]]=0;
    desc=[]
    print("Harvesting profile data...")
    for i in tqdm(range(len(users))):
    	desc.append(api.get_user(users[i]).description)
    	desc[i]=desc[i].lower();
    	for j in range(len(regex)):
    		r=regex[j].search(desc[i]);
    		if(r is not None):
    			tweetCount[keyWords[j]]=tweetCount[keyWords[j]]+count[users[i]]

    #plot bar graph
    #x=np.arange(len(keywords));
    #y=[]
    #for i in range(len(x)):
    #	y.append(tweetCount[keyWords[j]]);
    #plt.bar(x,y)
    #plt.show();

except Exception:
    traceback.print_exc()
    sys.exit(1)