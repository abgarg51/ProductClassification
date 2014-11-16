from gensim import corpora, models, similarities
import util

all_sources = ['amazon']
tree_category = 'books'
corpus, y = util.read_from_sources(all_sources, tree_category = tree_category, max_examples = 5000)

reviews = corpus[all_sources[0]]

stoplist = set('for a of the and to in'.split())
texts = [[word for word in r.lower().split() if word not in stoplist]
          for r in reviews]


dictionary = corpora.Dictionary(texts)

corpus = [dictionary.doc2bow(text) for text in texts]

model = models.hdpmodel.HdpModel(corpus, id2word=dictionary)

corpus_eval =  model.inference(corpus)

model.show_topics(100)