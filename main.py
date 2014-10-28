import regression, util, features, pandas as pd

if __name__  == '__main__':
	# read the data set
	dataset = util.load_data(source_file = 'amazon_review_test.txt')
	# extract the reviews and convert reviews into features. features is a list of sparse dicts
	reviews = [d['review'] for d in dataset]
	print 'Extracting features...'

	feature_extractor = features.BagOfWords()
	features = [dict(feature_extractor.extract_features(r)) for r in reviews]

	# put features into a pandas dataframe and fill 0 entries
	X = pd.DataFrame(features).fillna(0)
	# set y to targets nodes
	y = [d['id'] for d in dataset]

	# load regression
	clf = regression.LogisticRegression()
	print 'running regression...'
	clf.fit(X, y)
	print 'done running regresion'
	predicted_y = clf.predict(X)
	print "Prediction success rate = %.4f"%(clf.classification_error(y))