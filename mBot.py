#
#	Markov chain bot
#
#	
#
import tweepy as t


f=open('data.txt');
s=f.readlines();
e=[];
t=[];
for i in range(len(s)):
	t.append(s[i].split());#first word from the database
	e.append(t[i][0]);#append it to array of first words

#this loop works out which words are duplicate so it can begin the p structure

for i in range(len(s)):
	for j,k in enumerate(e):
		if(k==e[i]):
			print(j);
