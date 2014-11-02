import regression, util, features, pandas as pd, sklearn

if __name__ == '__main__':
    master_source = 'amazon'
    external_sources = ['twitter', 'ebay']
    tree_category = 'books'

    dataset = {}
    corpus = {}
    X = {}
    y = {}

    limit = 1000

    # load data from all the sources
    for source in [master_source] + external_sources:
        source_file = '%s_%s.dat'%(source, tree_category)
        print 'Loading %s data for %s from %s'%(tree_category, source, source_file)
        dataset[source] = util.load_data(source_file = source_file)
        # corpus is a list of all the reviews
        corpus[source] = [d['review'] for d in dataset[source]][:limit]
        y[source] = [d['id'] for d in dataset[source]][:limit]
        
    # Create feature extractor for master_source
    master_vectorizer = features.TfidfVectorizer(min_df=1)

    # Create feature matrix for master_source
    X[master_source] = master_vectorizer.fit_transform(corpus[master_source])

    # split test/train for master_source
    X_train, X_test, y_train, y_test = sklearn.cross_validation.train_test_split(X[master_source], y[master_source], test_size = 0.3, random_state = 42)
    assert set(y_train) == set(y_test), 'Not all labels are in both test and train. Try different random seed'

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
