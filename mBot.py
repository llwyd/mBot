#
#	Markov chain bot
#
#	
#
import tweepy as t
import collections
import random as r

f=open('data.txt');
s=f.readlines();
e=[];
t=[];
for i in range(len(s)):
	t.append(s[i].split());#first word from the database
	e.append(t[i][0]);#append it to array of first words

#this loop works out which words are duplicate so it can begin the p structure
d={};#define dictionary, this will hold each word and the location
for i in range(len(s)):
	#d[e[i]]=[t[i][1]];
	d[e[i]]=[]
	for j,k in enumerate(e):
		if(k==e[i]):
			d[e[i]].append(t[j][1]);

size=6;
d0={};
for i in range(len(s)):
	for p in range(size):
		d0[t[i][p]]=[]
		for j,k in enumerate(t[i]):
			if(k==t[i][p]):
				d0[t[i][p]].append(t[i][j+1]);

