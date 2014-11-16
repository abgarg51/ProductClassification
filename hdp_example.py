from gensim import corpora, models, similarities
import util

all_sources = ['amazon']
tree_category = 'books'
corpus, y = util.read_from_sources(all_sources, tree_category = tree_category, max_examples = 5000)

cleaned_reviews = [util.clean_sentence(review.encode('ascii', 'ignore')) for review in reviews]

# gensim expects each example to be a list of words, instead of a long string
texts = [[word for word in r.split()] for r in cleaned_reviews]

dictionary = corpora.Dictionary(texts)

corpus_bow = [dictionary.doc2bow(text) for text in texts]

model = models.hdpmodel.HdpModel(corpus_bow, id2word=dictionary)

corpus_eval =  model.inference(corpus_bow)

model.show_topics(100)