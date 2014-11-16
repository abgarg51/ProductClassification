from gensim import corpora, models, similarities
import util

all_sources = ['amazon']
tree_category = 'books'
corpus, y = util.read_from_sources(all_sources, tree_category = tree_category, max_examples = 5000)

reviews = corpus[all_sources[0]]

cleaned_reviews = [util.clean_sentence(review.encode('ascii', 'ignore')) for review in reviews]

# gensim expects each example to be a list of words, instead of a long string
texts = [[word for word in r.split()] for r in cleaned_reviews]

dictionary = corpora.Dictionary(texts)

corpus_bow = [dictionary.doc2bow(text) for text in texts]

tfidf = models.TfidfModel(corpus_bow)
corpus_tfidf = tfidf[corpus_bow]

# don't use this - HPD with TFIDF with crash your computer
# model = models.hdpmodel.HdpModel(corpus_bow, id2word=dictionary, T = 20)

model = models.ldamodel.LdaModel(corpus_tfidf, id2word=dictionary, num_topics = 20)

topic_distributions = list(model[corpus_tfidf])

# print_topic(topicid, topn=10)¶
model.print_topic(10)

#$print_topics(num_topics=10, num_words=10)