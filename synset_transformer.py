from nltk.corpus import wordnet as wn
from util import remove_punctuation, remove_stopwords, load_data, write_data
import unicodedata

def synset_word(word):
	synsets = wn.synsets(word)
	return set().union(*[s.lemma_names() for s in synsets])

def synset_review(review):
	review = unicodedata.normalize('NFKD', review).encode('ascii','ignore')
	review = remove_stopwords(remove_punctuation(review.lower()))
	words = review.split()
	return ' '.join([' '.join(synset_word(word)) for word in words])


if __name__ == '__main__':
	input_files = ['%s_electronics.dat'%source for source in ['amazon', 'ebay', 'twitter']]
	for input_filename in input_files:
		dataset = load_data(input_filename)
		for d in dataset:
			d['wordnet_expansion'] = synset_review(d['review'])
		output_filename = input_filename.split('.')[0] + '_expanded' + '.dat'
		write_data(dataset, output_filename)
