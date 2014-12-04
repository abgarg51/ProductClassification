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
# run this script with -c <category name> -w <weight> -n <word count>
# <weight> is the weight of words in original tweet as opose to newly expended words, 
# the original stirng will be simply multiplyed <weight> times
# <word count> is the number of words that will be used to extend each hashtag
#
# script will generate ./data/HashTags_Other_Tweets_<categoryName>.dat
# in which each line is a jason object, inside is a dict with 2 keys:
# "hashTag" is the hash
# "wordCounter" is the counter of each word appeared in tweetes that had that hashtag.
#
# Then it will create a file ./data/twitter_electronics_he_w<5>_n<word count>.dat
# I would create simbolic links of ./data/twitter_electronics.dat to different files to test and compare them.
####################

def getListOfHashtagsFromCorpus(category):
	hashSet = set()
	tweetFileName = "./data/twitter_%s.dat"%category
	global dataset
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
		hashDict[hashtag] = wordcount
		outFile.write(unicode(json.dumps(out_obj, ensure_ascii=False)))
		outFile.write(unicode('\n'))

def loadHashDictFromFile(hashDictFileName):
	with open(hashDictFileName, 'r+') as f:
		tempdataset = [json.loads(line) for line in f]
	for line in tempdataset:
		hashDict[line['hashTag']] = line['wordCounter']
	print "loaded hash wordcount from file with lines: ", len(hashDict)
	corpusHashTags = getListOfHashtagsFromCorpus(options.category)
	

def createNewDataWithExtendedHashtags(category, weightOfOldContent, numWordsPerHashtag, normalizeHashWeight):
	#normalizeHashWeight not implemented..
	outFileName = "./data/twitter_%s_he_w%d_n%d.dat"%(category,weightOfOldContent,numWordsPerHashtag)
	print "Creating new file with extended hashtag: " , outFileName
	extendedLineCount = 0
	processedLineCount = 0
	outFile = io.open(outFileName, "w", encoding='utf-8')
	for line in dataset:
		processedLineCount += 1
		review = line['review']
		catgoryNodeId = line['id']
		reviewWords = line['review'].replace('\n',' ').split(' ')
		extends = u''
		for word in reviewWords:
			if "#" in word:
				originalHashtag = word[word.index('#'):].lower()
				extendedWordCounters = Counter()
				if originalHashtag in hashDict.keys() and originalHashtag not in [u'#amazonwishlist', u'#amazongiveaway', u'#amazoncart']:
					extendedLineCount += 1
					extendedWordCounters = Counter(hashDict[originalHashtag])
					extendedWordTuples = extendedWordCounters.most_common(numWordsPerHashtag)
					extendedWordsList = [x[0] for x in extendedWordTuples]
					extendingWordsString = u' '.join(extendedWordsList)
					extends = extends + u' ' + extendingWordsString
					#print "extending: ", originalHashtag.encode('utf-8')
				#else:
					#print "Do not have extention for hashtag: ", originalHashtag.encode('utf-8')

		review = (review + u' ') * weightOfOldContent + extends
		out_obj = {'review':review, 'id':catgoryNodeId}
		outFile.write(unicode(json.dumps(out_obj, ensure_ascii=False)))
		outFile.write(unicode('\n'))
		if processedLineCount % 1000 == 0:
			print '.',
				#print "extending ", word.encode('utf-8'), " with: ", newReviewString.encode('utf-8')

	print "Extended hash count", extendedLineCount



if __name__ == "__main__":
	parser = OptionParser('Usage: python hashtag_reader.py -c <category name>')
	parser.add_option("-c", "--category", dest="category",
                    default='',
                  help="category name you want to process")
	parser.add_option("-w", "--weight", dest="weightOfOldContent",
                    default=5,
                  help="weight for original words in the tweet")
	parser.add_option("-n", "--numwords", dest="numWordsPerHashtag",
                    default=20,
                  help="number of words extended per hash")
	parser.add_option("-f", "--flush", action="store_true", dest="forceFlush",
                  help="force flush the hash dict file and create new one")
	(options, args) = parser.parse_args()
	if not options.category:
		parser.error('please specify category name')
	print "loading/generating twitter hashtag word dict for: ", options.category

	dataset = [] #global to hold the dataset for processing.
	hashDict = {}  #global dict to hold hash -> word counter

	hashDictFileName = "./data/HashTags_Other_Tweets_%s.dat"%options.category

	if not os.path.isfile(hashDictFileName) or options.forceFlush:
		createHashtagWordDictForCategory(options.category)
	else:
		loadHashDictFromFile(hashDictFileName)


	createNewDataWithExtendedHashtags(options.category, int(options.weightOfOldContent), int(options.numWordsPerHashtag), True)

