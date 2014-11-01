import regression, util, features, pandas as pd, numpy as np, sklearn
import matplotlib.pyplot as plt

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

	# split test/train
	X_train, X_test, y_train, y_test = sklearn.cross_validation.train_test_split(X, y, test_size = 0.3, random_state = 42)
	assert set(y_train) == set(y_test), 'Not all labels are in both test and train. Try different random seed'

	# load regression
	clf = regression.LogisticRegression()
	print 'running regression...'
	clf.fit(X_train, y_train)

	print "Training Score = %.4f"%(clf.score(X_train, y_train))
	print "Test Score = %.4f"%(clf.score(X_test, y_test))

	# generate confusion matrix
	y_pred = clf.predict(X_test)
	cm = sklearn.metrics.confusion_matrix(y_test, y_pred)

	# normalize along the row
	row_sums = cm.sum(axis=1)
	cm_normalized = 1.0 * cm / row_sums[:, np.newaxis]

	# plot confusion matrix
	plt.figure(1, figsize=(15,12))
	plt.matshow(cm_normalized,fignum=1)
	plt.title('Confusion matrix')
	plt.colorbar()
	plt.ylabel('True label')
	plt.xlabel('Predicted label')
	plt.show()