from gensim import corpora, models, similarities
import util

all_sources = ['amazon']
tree_category = 'books'
corpus, y = util.read_from_sources(all_sources, tree_category = tree_category, max_examples = 5000)

reviews = corpus[all_sources[0]]

reviews = [util.clean_sentence(review) for review in reviews]

dictionary = corpora.Dictionary(reviews)

corpus_bow = [dictionary.doc2bow(review) for review in reviews]

model = models.hdpmodel.HdpModel(corpus_bow, id2word=dictionary)

corpus_eval =  model.inference(corpus_bow)

model.show_topics(100)