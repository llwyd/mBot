#
#
#
#   markovMagpie
#		v0.2
#
#
#import libraries
import tweepy
import random as r
import time
import re
import tweet_store
from tqdm import tqdm
import settings
import numpy as np
import os
import datetime as dt
import sys
import twitter as tw
import json
import collections
import pickle

def post_tweet(statusmsg, info):
	auth = tweepy.OAuthHandler(info['ck'], info['cs'])
	auth.set_access_token(info['at'], info['ats'])

	try:
		api.update_status(status=statusmsg)
		print('Tweet Successful')
	except Exception:
		# Stops everything crashing if there is a connection issue.
		print('Tweet Unsuccessful')


def build_word(e,d,d0):
	r.seed(dt.datetime.now());
	pf0 = ""
	# print("Building output...", end="", flush=True)
	rFlag = True  # flag to check for repeat
	while rFlag:
		f0 = e[r.randint(0, len(e) - 1)]  # first word
		if len(d[f0]) > 1:
			rFlag = False
	rFlag=True;
	while rFlag:
		f1 = d[f0][r.randint(0, len(d[f0]) - 1)]  # second word
		if len(d[f0]) > 1:
			rFlag = False
	# f2 = d0[f1][r.randint(0, len(d0[f1]) - 1)]  # anything after can follow this
	output = f0 + " " + f1
	op = f1
	if len(d0[f1]) > 0:
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
	#lastchar = output[len(output) - 1]
	lastchar=output[-1];
	#print(output);
	#This doesnt work, wtf
	testOut=output;
	if (output[-1] != '.') and (output[-1] != '?') and (output[-1] != '!'):
		output += '.'
	return output,testOut


try:
	# number of tweets to read (capped at 200 by twitter)
	#numTweet = settings.get_tweet_history_limit()
	# time between tweets in seconds
	#delay = settings.get_tweet_frequency()
	# size of overall storage buffer
	buffSize = 1000
	# current position of buffer
	buffPos = 0
	#master list of tweets
	master = []
	# key, array of first values
	e = []
	t = []
	# define dictionary, this will hold each word and the location
	d = {}
	d0 = {}
	# Filter for removing punctuation (except sentence endings)
	puncFilter = str.maketrans('', '', '…\"$%&\'()*+,-/:;<=>@[\\]‘^_`{|}~')
	#flag for enabling tweets
	active=settings.get_tweet_post();
	#flag for enabling punctuation filter
	punc=settings.get_filter_punc();	
except Exception as ex:
	print(ex);
	sys.exit(1);


f=open('data.txt');
s=f.readlines();
f.close();

#Remove textless image only tweets;
purgeList=[];
for i in range(len(s)):
	if(s[i][0:5]=="https"):
		purgeList.append(i);
for i in range(len(purgeList)-1,-1,-1):
	s.pop(purgeList[i]);
#punctuation filter
if(punc==True):
	for i in range(len(s)):
		s[i]=s[i].translate(puncFilter);
#Split array of words
for i in range(len(s)):
	t.append(s[i].split());
	if(t[i][-1][0:5]=="https"):
		t[i].pop(-1);
	if(t[i][-1][0:5]=="https"):
		t[i].pop(-1);
#Remove single word tweets
purgeList=[];
for i in range(len(t)):
	if(len(t[i])<2):
		purgeList.append(i);
for i in range(len(purgeList)):
	t.pop(purgeList[i]);
#--------------------------------------
#   begin filtering of firstWords
#--------------------------------------
for i in range(len(t)):
	dup=False;
	for j in range(len(e)):
		if(t[i][0]==e[j]):
			dup=True;
			break;
	if(dup==False):
		e.append(t[i][0]);
#--------------------------------------
#	Filter second words
#--------------------------------------
#check if the first word already exists in the dictionary
for i in range(len(e)):
	if((e[i] in d))==False:
		d[e[i]]=[];
#Create dictionary of first words and second words
for i in range(len(t)):
	dup=False
	#print(i);
	for j in range(len(d[t[i][0]])):
		if(d[t[i][0]][j])==t[i][1]:
			dup=True;
			break;
	if(dup!=True):
		d[t[i][0]].append(t[i][1]);
#--------------------------------------
#	Other Words
#--------------------------------------
#check if word already exists
for i in range(len(s)):
	if s[i] is None:
		continue
	for p in range(1,len(t[i])):
		if not (t[i][p] in d0.keys()):
			d0[t[i][p]] = [];
#add new words to database
for i in range(len(s)):
	if s[i] is None:
		continue
	for j in range(2,len(t[i])):
		dup=False
		for k in range(len(d0[t[i][j-1]])):
			if d0[t[i][j-1]][k]==t[i][j]:
				dup=True;
				break;
		if(dup!=True):
			d0[t[i][j-1]].append(t[i][j]);
output,meow = build_word(e,d,d0)
while len(output) > 280:
	output,meow = build_word(e,d,d0)
print(output+"\n");

#post_tweet(output,tweetStuff);

#with open ("database.txt","wb") as fp:
#	pickle.dump(s,fp);

