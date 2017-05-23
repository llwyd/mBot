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

size=10;
d0={};
for i in range(len(s)):
	for p in range(len(t[i])):
		d0[t[i][p]]=[]
		for j,k in enumerate(t[i]):
			if((k==t[i][p])and(j!=len(t[i])-1)):
				d0[t[i][p]].append(t[i][j+1]);




f0=e[r.randint(0,len(s)-1)];#first word
f1=d[f0][r.randint(0,len(d[f0])-1)]#second word
f2=d0[f1][r.randint(0,len(d0[f1])-1)]#anything after can follow this
output=f0+" "+f1+" "+f2;
op=f2;
outLen=r.randint(5,10);

end=False;


while end!=True:
	try:
		on=d0[op][r.randint(0,len(d0[op])-1)]#output new
		op=on;#output previous
		output=output+" "+ op;
		if(len(d0[op])==0):
			output=output+".";
			end=True;
	except:
		output=output+".";	
		break;
print(output);	
