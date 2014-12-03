import json
import io
import sys
from collections import Counter

#####  MAIN  #######
# download this file: https://s3.amazonaws.com/stanford-project/p1/HashTags_Other_Tweets.json.gz
# unzip it to ./data/
# run this script with no argument
# it will generate ./data/HashTags_Other_Tweets.dat
# in which each line is a jason object, inside is a dict with 2 keys:
# "hashTag" is the hash
# "wordCounter" is the counter of each word appeared in tweetes that had that hashtag.
####################

if __name__ == "__main__":
	hashtagDataFileName = "./data/HashTags_Other_Tweets.json"
	lineCount = 0
	outFileName = "./data/HashTags_Other_Tweets.dat"
	outFile = io.open(outFileName, "w", encoding='utf-8')
	wordDict = {}
	tagCounter = Counter()
	stopTags = {"#RT","#rt", "#FF", "#TEAMFOLLOWBACK","#teamfollowback", "#TeamFollowBack","#teamautofollow",  "#TFW", "#TFB", "#RETWEET", "#Follow", "#FOLLOW", "#HITFOLLOWSTEAM", "#followme","#RETWEEET", "#FOLLOWBACK", "#IFOLLOWBACK", "#followback", "#TFBJP", "#Followback", "#ANOTHERFOLLOWTRAIN", "#AnotherFollowTrain","#Follow2BeFollowed"}  #get ride of some tags that do not mean anything.
	with open(hashtagDataFileName, 'r+') as data_file:
		for line in data_file:
			lineCount += 1

			try:
				item = json.loads(line.strip()[:-1])
			except ValueError, e:
				print "Format error: ", line
				continue
			reviews = item['conversation_text'];
			bagOfWord = set(reviews.split(' '))
			hashTags = item['conversation_hashtags'];
			wordCount = Counter()
			for word in bagOfWord:
				wordCount[word] += 1 
			if not isinstance(hashTags, list):
				print "hash tags is not a list", hashTags
				continue
			for hash in hashTags:
				if hash in stopTags or u"follow" in hash.lower().encode('utf8'):
					continue
				tagCounter[hash] += 1;
				
				if wordDict.has_key(hash):
					wordDict[hash] = wordDict[hash] + wordCount
				else:
					wordDict[hash] = wordCount

			if lineCount %10000 == 0:
				print "Processed Lines: ", lineCount
				print tagCounter.most_common(300)


		for key in wordDict.keys():
			out_obj = {'hashTag':key, 'wordCounter':wordDict[key]}
			outFile.write(unicode(json.dumps(out_obj, ensure_ascii=False)))
			outFile.write(unicode('\n'))
			#print key.encode('utf-8'), ": ", wordDict[key].most_common(10), "..."

		print tagCounter.most_common(300)
