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
import nltk
#
#
#
#   markovMagpie statistical analysis
#      v0.2
#
#
#
if os.path.isfile("database.pkl"):
    print("Loading tweet database...")
    with open("database.pkl", "rb") as fp:
        s = pickle.load(fp)
else:
    print("Database not found, quitting...")
    sys.exit()

e = []
t = []
# define dictionary, this will hold each word and the location
d = {}
d0 = {}
# Filter for removing punctuation (except sentence endings)
puncFilter = str.maketrans('', '', '…\"$%&\'()“”"*+-/<=>[\\]^_`{|}~')
# flag for enabling tweets
active = settings.get_tweet_post()
# flag for enabling punctuation filter
punc = settings.get_filter_punc()


# Remove textless image only tweets;
purgeList = []
for i in tqdm(range(len(s))):
    if s[i][0:5] == "https":
        purgeList.append(i)
for i in range(len(purgeList) - 1, -1, -1):
    s.pop(purgeList[i])

# punctuation filter
if punc:
    print("Punctuation Filtering...")
    for i in range(len(s)):
        s[i] = s[i].translate(puncFilter)

# Replace &
for i in range(len(s)):
    s[i] = s[i].replace("amp;", "and")

# Split array of words
for i in range(len(s)):
    t.append(s[i].split())
    if t[i][-1][0:5] == "https":
        t[i].pop(-1)
    if t[i][-1][0:5] == "https":
        t[i].pop(-1)

# Remove https links from everywhere...
linkRegex = re.compile(r'https')
for i in range(len(t)):
    purgeList = []
    for j in range(len(t[i])):
        mo = linkRegex.search(t[i][j])
        if mo is not None:
            purgeList.append(j)

    for j in range(len(purgeList) - 1, -1, -1):
        t[i].pop(purgeList[j])

# Remove single word tweets
purgeList = []

for i in range(len(t)):
    if len(t[i]) < 3:
        purgeList.append(i)
for i in range(len(purgeList) - 1, -1, -1):
    t.pop(purgeList[i])

# --------------------------------------
#   begin filtering of firstWords
# --------------------------------------
print("Building array of n[0]...")
for i in tqdm(range(len(t))):
    dup = False
    for j in range(len(e)):
        if t[i][0] == e[j]:
            dup = True
            break
    if not dup:
        e.append(t[i][0])

# --------------------------------------
#   Filter second words
# --------------------------------------
# check if the first word already exists in the dictionary
print("Building array of n[1]...")
print("	Check if word already exists...")
for i in tqdm(range(len(e))):
    if not (e[i] in d):
        d[e[i]] = []

# Create dictionary of first words and second words
print("	Building array of n[0] and n[1]...")
for i in tqdm(range(len(t))):
    dup = False
    # print(i);
    for j in range(len(d[t[i][0]])):
        if (d[t[i][0]][j]) == t[i][1]:
            dup = True
            break
    if not dup:
        d[t[i][0]].append(t[i][1])

# --------------------------------------
#   Other Words
# --------------------------------------
print("Building array of n[1:k]...")
# check if word already exists
print("	Check if word already exists...")
for i in tqdm(range(len(t))):
    if t[i] is None:
        continue
    for p in range(1, len(t[i])):
        if not (t[i][p] in d0.keys()):
            d0[t[i][p]] = []

# add new words to database
print("	Add new words to database...")
for i in tqdm(range(len(t))):
    if t[i] is None:
        continue
    for j in range(2, len(t[i])):
        dup = False
        for k in range(len(d0[t[i][j - 1]])):
            if d0[t[i][j - 1]][k] == t[i][j]:
                dup = True
                break
        if not dup:
            d0[t[i][j - 1]].append(t[i][j])
#Some minor stats
print("----------------------------------------")
print("	Basic stats...")
countNumber=100
hashRegex=re.compile(r'#');
hashTags=[]
for i in range(len(t)):
    purgeList = []
    for j in range(len(t[i])):
        mo = hashRegex.search(t[i][j])
        if mo is not None:
        	hashTags.append(t[i][j])
hashCount=Counter(hashTags).most_common(countNumber);
#print("Number of starting words: "+str(len(e)));
maxKeys=0
maxKeyLoc=0
for i in tqdm(range(len(e))):
	currentLength=len(d[e[i]]);
	if(currentLength>maxKeys):
		maxKeys=currentLength
		maxKeyLoc=i
#print("The word '"+e[maxKeyLoc]+"' has the most following words ("+str(maxKeys)+") entries")
masterWordList=[];
wordCount=collections.Counter()
for i in tqdm(range(len(t))):
	wordCount=wordCount+Counter(t[i]);

mostCommonWords=wordCount.most_common(countNumber);
print("----------------------------------------")
print(" 	Print Data")
print("----------------------------------------")
print("Number of starting words: "+str(len(e)));
print("The word '"+e[maxKeyLoc]+"' has the most following words ("+str(maxKeys)+") entries")
print("The most common "+str(countNumber)+"  words are: ")
for i in range(len(mostCommonWords)):
	print("	"+str(mostCommonWords[i]))
print("The most common "+str(countNumber)+"  hashtags are: ")
for i in range(len(hashCount)):
	print("	"+str(hashCount[i]))