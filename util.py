"""
	util.py
	File contains utilities
"""

import sys, os, json, re, string
from stemming.porter2 import stem
data_directory = 'data' # directory that all data is stored in

stopwords = []

def remove_punctuation(sentence):
  table = string.maketrans("","")
  return sentence.translate(table, string.punctuation)

with open('stopwords.txt', 'r') as f:
  for line in f:
    stopwords.append(remove_punctuation(line.strip()))


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

def remove_stopwords(sentence):
  pattern = re.compile(r'\b(' + r'|'.join(stopwords) + r')\b\s*')
  sentence = pattern.sub('', sentence)
  return sentence

def clean_sentence(sentence, stem = True, stopwords = True, punctuation = True, lower = True):
  if isinstance(sentence, unicode):
    sentence = sentence.encode('ascii', 'ignore')
  return remove_stopwords(stem_sentence(remove_punctuation(sentence.lower()))) 


"""
  Info
"""
info = """Index:  0   Appliances
Index:  1   ArtsAndCrafts
Index:  2   Automotive
Index:  3   Baby
Index:  4   Beauty
Index:  5   Books
Index:  6   Music
Index:  7   Collectibles
Index:  8   Movies & TV
Index:  9   Electronics
Index:  10  Grocery
Index:  11  HealthPersonalCare
Index:  12  Tools
Index:  13  KindleStore
Index:  14  Kitchen
Index:  15  LawnAndGarden
Index:  16  Magazines
Index:  17  Everything Else
Index:  18  MobileApps
Index:  19  MusicalInstruments
Index:  20  OfficeProducts
Index:  21  Software
Index:  22  SportingGoods
Index:  23  Toys
Index:  24  VideoGames
"""
temp = [x.split() for x in info.split('\n')]
index_to_name_dict = {row[1]: ''.join(row[2:]).lower() for row in temp if len(row) > 2}
all_sources = ['amazon', 'ebay', 'twitter']

# handle browse node to string
import csv
node_to_string = {}
with open('scratch/amazon_category_names.txt', 'r+') as csvfile:
  reader = csv.reader(csvfile, delimiter='\t')
  for row in reader:
    tree_category, node, name = row
    node_to_string[int(node)] = name.strip()

if __name__ == '__main__':
  sentence = 'running! Down.. the street? some more words'
  print 'ORIGINAL:', sentence 
  print 'STEMMING:', stem_sentence(sentence)
  print 'STOPWORDS:', remove_stopwords(sentence)
  print 'PUNCUTATION:', remove_punctuation(sentence)
  print 'ALL:', clean_sentence(sentence)
  print node_to_string
