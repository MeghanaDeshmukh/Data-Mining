import sys
import csv
import math

data = {}
## outPut[currIndex]
## freqSets[freqIndex]
def getComb(freqSets, combLen, outPut, freqIndex, allComb, currIndex, infreq):
	##Current combination is ready, print it  
	if currIndex	>= combLen:
		## Remove the infrequent sets
		for key in infreq.keys():
			if set(key.split(";")).issubset(outPut):
				outPut.pop(len(outPut)-1);
				return;
		if ";".join(outPut) not in allComb:
			allComb.append(";".join(outPut));
		outPut.pop(len(outPut)-1);
		return;
		
	##  When no more elements are there to put in data[]  
	if freqIndex >= len(freqSets):
		return
	
	## current is included, put next at next location  
	if len(outPut) > currIndex:
		outPut[currIndex] =  list(freqSets.keys())[freqIndex];
	else: 
		outPut.insert(currIndex,  list(freqSets.keys())[freqIndex]);
	getComb(freqSets, combLen, outPut, freqIndex+1, allComb,currIndex+1, infreq)
	
	## current is excluded, replace it with next (Note that  
    ## i+1 is passed, but index is not changed)  
	getComb(freqSets, combLen,  outPut, freqIndex+1, allComb,currIndex, infreq)
	
def getSupport(sets, infreq, patterns): 
	supp = {};
	newDict = {};
	freqCnt = 0;
	for i in range (0, len(sets)):
		cats = [];
		cats = sets[i].split(";");
		count = 0;
		prune = 0;

		if prune == 0:
			for tid in data.keys():
				if set(cats).issubset(data[tid]):
					count += 1;
		supp[i] = count;
		if supp[i] <= 771:
			infreq[sets[i]] = supp[i];
		else: 
			patterns.write("%d:%s\n" % (supp[i],sets[i]))
			freqCnt += 1;
			for i in range (0, len(cats) ):
				if cats[i] in newDict.keys():
					newDict[cats[i]] += 1
				else:
					newDict[cats[i]] = 1
	return (supp, infreq, freqCnt);
	
#def prune():
	


def readData():
	trans = {}
	items = {}

	f = open("categories.txt", "r");
	patterns = open("patterns.txt", "w+");
	check = open("check.txt", "w+");
	count = 0;
	maxLen = 0;
	for row in f:
		if (len(row) > 0):
			row = row.split("\n");
			data[count] = []
			data[count] = row[0].split(";");
			for i in range (0, len(data[count]) ):
				if maxLen < len(data[count]):
					maxLen = len(data[count]);
				if data[count][i] in items.keys():
					items[data[count][i]] += 1
					trans[data[count][i]].append(count);
				else:
					items[data[count][i]] = 1;
					trans[data[count][i]] = [count]
			count +=1;
			
	### Part1.		
	for i in items.keys():
		if items[i] > 771:
			patterns.write("%d:%s\n" % (items[i],i))
		else:
			del trans[i];
	check.close()

	temp = [];
	allComb=[]
	infreq = {};
	freqCnt = 1;
	k = 2;
	print("Max len of trans: ", maxLen);

	## Part2
	## Now, loop till all the supp are obtained
	while freqCnt > 0:
		print("In while: k is ", k, "len of dict - ", len(trans));
		getComb(trans, k, temp, 0, allComb,0, infreq);
		print("Combinations to go through: ",  len(allComb));
		(support, infreq, freqCnt) = getSupport(allComb, infreq, patterns);
		print("Total combinations: ", len(allComb));
		print("The supprot is: ",len(support));
		print("The infreq is: ",len(infreq));
		allComb.clear();
		print("For K: ", k, " The frequent count is :",freqCnt, len(trans));
		k += 1;
		if k > maxLen:
			freqCount = 0;
			print("Exceeded Max len of all the transaction");
		
		
	patterns.close();

	
	
def main():
	readData();
	
	
main();