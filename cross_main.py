"""
    This script will only work if you've generated all the data
    python data_reader.py amazon 5 data/amazon_books.dat
    python data_reader.py ebay 5 data/ebay_books.dat
    python data_reader.py twitter 5 data/twitter_books.dat
"""

import regression, util, features, pandas as pd, sklearn, numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import pyplot as plt

def read_from_sources(sources, tree_category, max_examples = 1000):
    # Return the an ordered pair of dicts, the Corpus for each source and the targets for each source
    dataset = {}
    corpus = {}
    y = {}
    for source in sources:
        source_file = '%s_%s.dat'%(source, tree_category)
        print 'Loading %s data for %s from %s'%(tree_category, source, source_file)
        dataset[source] = util.load_data(source_file = source_file)
        # corpus is a list of all the reviews
        corpus[source] = [d['review'] for d in dataset[source]][:max_examples]
        y[source] = [d['id'] for d in dataset[source]][:max_examples]
    return corpus, y

def learn_cross_domain(master_source, external_sources, corpus, y, max_examples = 1000):  
    # Create feature extractor for master_source
    master_vectorizer = features.TfidfVectorizer(min_df=1)

    # Create feature matrix for master_source
    X = {}
    X[master_source] = master_vectorizer.fit_transform(corpus[master_source])

    # split test/train for master_source
    random_state = 42
    while True:
        X_train, X_test, y_train, y_test = sklearn.cross_validation.train_test_split(X[master_source], y[master_source], test_size = 0.3, random_state = random_state)
        if set(y_train).issuperset(set(y_test)):
            break
        else:
            random_state += 1
            print 'Training labels are not a superset of the testing labels. Trying different random seed: %d'%random_state
            

    # Create regression and train on master_source training set
    clf = regression.LogisticRegression()
    print 'running regression...'
    clf.fit(X_train, y_train)

    # Report test and train for master_source
    print "Training score for %s on %s = %.4f"%(master_source, master_source, clf.score(X_train, y_train))
    print "Test score for %s on %s = %.4f"%(master_source, master_source, clf.score(X_test, y_test))

    # Deal with external sources
    for source in external_sources:
        # create a vectorizer that filters on the vocabulary of the vectorizer for the master source
        # *** If you do not do this - the fitter won't be able to predict words that it has not scored
        vectorizer = features.TfidfVectorizer(min_df=1, vocabulary = master_vectorizer.vocabulary_.keys())
        # create feature matrix for external source
        X[source] = vectorizer.fit_transform(corpus[source])
        # Report the scores
        print "%s trained on %s score = %.4f"%(source, master_source, clf.score(X[source], y[source]))

    #import pdb; pdb.set_trace()
    # plotting
    pp = PdfPages('plots_trained_on_%s.pdf'%master_source)
    for i, source in enumerate([master_source] + external_sources):
        # generate confusion matrix
        y_pred = clf.predict(X[source])
        cm = sklearn.metrics.confusion_matrix(y[source], y_pred)

        # normalize along the row
        row_sums = cm.sum(axis=1)
        cm_normalized = 1.0 * cm / row_sums[:, np.newaxis]

        # plot confusion matrix
        plt.figure(i, figsize=(15,12))
        plt.clf()
        plt.matshow(cm_normalized,fignum=i)
        plt.title('Confusion matrix for %s trained on %s'%(source.upper(), master_source.upper()))
        plt.colorbar()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        pp.savefig()
    pp.close()
if __name__ == '__main__':
    all_sources = ['amazon', 'twitter', 'ebay']
    tree_category = 'books'
    combos = [('amazon', ['twitter', 'ebay'], tree_category),
                ('twitter', ['amazon', 'ebay'], tree_category),
                ('ebay', ['amazon', 'twitter'], tree_category),
                ]

    corpus, y = read_from_sources(all_sources, tree_category = tree_category, max_examples = 10000)
    for master_source, external_sources, tree_category in combos:
        learn_cross_domain(master_source, external_sources, corpus, y)


    """
    Example for a single run
    master_source = 'amazon'
    external_sources = ['twitter', 'ebay']
    tree_category = 'books'
    learn_cross_domain(master_source, external_sources, tree_category)
    """

    
