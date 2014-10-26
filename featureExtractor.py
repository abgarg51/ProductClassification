"""feature extractor
takes in review and returns featuers using bag of words
"""
import collections 
def extractFeatures(review):
	bag = collections.Counter()
	for word in review.split():
		bag[word] += 1
	return bag

print extractFeatures("A counter tool is provided to support convenient and rapid tallies")