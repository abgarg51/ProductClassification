"""feature extractor
takes in review and returns featuers using bag of words
"""
import collections 

class FeatureExtractor(object):
	"""
	LearningAlgorithm is an abstract class. All learning algorithms should have the following methods
	"""
	def __init__(self):
		pass
	def extractFeatures(self, text):
		pass

class BagOfWords(FeatureExtractor):
	"""
	Bag of words returns count of words
	"""
	def __init__(self):
		pass

	def extract_features(self, text):
		words = text.split()
		bag = collections.Counter(words)
		return bag

if __name__ == '__main__':
	featureExtractor = BagOfWords()
	print 'hi'
	print featureExtractor.extract_features("A counter tool is provided to support convenient and rapid tallies")