import json
import io
import sys
import os
import time
import shutil
from collections import Counter
from optparse import OptionParser

#####  MAIN  #######
# download this file: https://s3.amazonaws.com/stanford-project/p1/HashTags_Other_Tweets.json.gz
# unzip it to ./data/
# run this script with -c <category name>
# it will generate ./data/HashTags_Other_Tweets_<categoryName>.dat
# in which each line is a jason object, inside is a dict with 2 keys:
# "hashTag" is the hash
# "wordCounter" is the counter of each word appeared in tweetes that had that hashtag.
####################

def getListOfHashtagsFromCorpus(category):
	hashSet = set()
	tweetFileName = "./data/twitter_%s.dat"%category
	with open(tweetFileName, 'r+') as f:
		dataset = [json.loads(line) for line in f]
	if len(dataset) == 0:
		print "Error, could not find twitter data file: ",  tweetFileName
		return set();
	for line in dataset:
		words = line['review'].replace('\n',' ').split(' ')
		for word in words:
			if "#" in word:
				word = word[word.index('#'):]
				hashSet.add(word.lower())
	return hashSet


def createHashtagWordDictForCategory(category):
	hashtagDataFileName = "./data/HashTags_Other_Tweets.json"
	corpusHashTags = getListOfHashtagsFromCorpus(category)
	corpusHashTagsList = list(corpusHashTags)
	fileDict = {}
	lineCount = 0
	tempDir = "./scratch/temphash_%s/"%category

	outFileName = "./data/HashTags_Other_Tweets_%s.dat"%category
	outFile = io.open(outFileName, "w", encoding='utf-8')

	try:
		shutil.rmtree(tempDir)
	except OSError as why:
		print str(why)

	os.makedirs(tempDir)
	for hashtag in corpusHashTags:
		tempFileName = tempDir + "%d"%corpusHashTagsList.index(hashtag)
		tmpFile = io.open(tempFileName, "w", encoding='utf-8')
		fileDict[hashtag] = tmpFile


	with open(hashtagDataFileName, 'r+') as data_file:
		for line in data_file:
			lineCount += 1
			if lineCount % 10000 == 0:
				print "Processed Line: ", lineCount, "/14800000"

			try:
				item = json.loads(line.strip()[:-1])
			except ValueError, e:
				print "Format error: ", line
				continue

			reviews = item['conversation_text'];
			hashTags = item['conversation_hashtags'];

			if not isinstance(hashTags, list):
				print "hash tags not a list", hashTags
				continue
			for hash in hashTags:
				if hash not in corpusHashTags:
					continue
				fileDict[hash].write(unicode(reviews))

	for hashtag in corpusHashTags:
		fileDict[hashtag].close()
		tempFileName = tempDir + "%d"%corpusHashTagsList.index(hashtag)
		tmpFile = io.open(tempFileName, "r", encoding='utf-8')
		fileDict[hashtag] = tmpFile

		wordcount = Counter(fileDict[hashtag].read().split())
		out_obj = {'hashTag':hashtag, 'wordCounter':wordcount}
		outFile.write(unicode(json.dumps(out_obj, ensure_ascii=False)))
		outFile.write(unicode('\n'))



if __name__ == "__main__":
	parser = OptionParser('Usage: python hashtag_reader.py -c <category name>')
	parser.add_option("-c", "--category", dest="category",
                    default='',
                  help="category name you want to process")
	(options, args) = parser.parse_args()
	if not options.category:
		parser.error('please specify category name')
	print "generating twitter hashtag word dict for: ", options.category
	createHashtagWordDictForCategory(options.category)

