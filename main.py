import regression, util, features, pandas as pd

if __name__  == '__main__':
	# read the data set
	dataset = util.load_data(source_file = 'amazon_review_test.txt')
	# corpus is a list of all the reviews
	corpus = [d['review'] for d in dataset]
	print 'Extracting features...'

	# use BagOfWords with TFIDF normalizationn
	vectorizer = features.TfidfVectorizer(min_df=1)
	# put features into a pandas dataframe and fill 0 entries
	X = vectorizer.fit_transform(corpus)
	# set y to targets nodes
	y = [d['id'] for d in dataset]

	# load regression
	clf = regression.LogisticRegression()
	print 'running regression...'
	clf.fit(X, y)
	print 'done running regresion'
	predicted_y = clf.predict(X)
	print "Prediction success rate = %.4f"%(clf.classification_error(y))