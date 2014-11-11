"""
	util.py
	File contains utilities
"""

import sys, os, json
from stemming.porter2 import stem
data_directory = 'data' # directory that all data is stored in

def load_data(source_file = 'amazon_review_test.txt'):
	print "loading data..."
	data_pathname = os.path.join(data_directory, source_file)
	with open(data_pathname, 'r+') as f:
		dataset = [json.loads(line) for line in f]
	print 'finished reading json'
	return dataset


def read_from_sources(sources, tree_category, max_examples = 1000):
    # Return the an ordered pair of dicts, the Corpus for each source and the targets for each source
    dataset = {}
    corpus = {}
    y = {}
    for source in sources:
        source_file = '%s_%s.dat'%(source, tree_category)
        print 'Loading %s data for %s from %s'%(tree_category, source, source_file)
        dataset[source] = load_data(source_file = source_file)
        # corpus is a list of all the reviews
        corpus[source] = [d['review'] for d in dataset[source]][:max_examples]
        y[source] = [d['id'] for d in dataset[source]][:max_examples]
    return corpus, y

def stem_sentence(sentence):
  """
    Given a sentence, return the stemmed version of the sentence.
  """
  words = sentence.split()
  stemmed_words = [stem(w) for w in words]
  stemmed_sentence = ' '.join(stemmed_words)
  return stemmed_sentence

def stem_corpus(corpus):
  """
    Given a corpus, a dict of lists (a list of reviews), return a stemmed version
    corpus['twitter'] = [long_list_of_reviews]
  """
  print 'Stemming Corpus...'
  stemmed_corpus = {source: [stem_sentence(review) for review in reviews] for source, reviews in corpus.items()}
  return stemmed_corpus

if __name__ == '__main__':
  sentence = 'running down the street'
  print stem_sentence(sentence)
