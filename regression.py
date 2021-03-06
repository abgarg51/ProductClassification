"""
	regression.py
	File contains all the learning algorithms that we will use
"""

from sklearn import linear_model
import pandas as pd, numpy as np


class LearningAlgorithm(object):
	"""
		LearningAlgorithm is an abstract class. All learning algorithms should have a fit method and a predict method
	"""
	def __init__(self):
		pass
	def fit(self, X, y):
		pass
	def predict(self, X):
		pass

class LogisticRegression(LearningAlgorithm):
	"""
	LogisticRegression implemented in sklearn
	"""
	def __init__(self):
		self.clf = linear_model.LogisticRegression()
		self.predicted_y = None

	def fit(self, X, y):
		self.clf.fit(X, y)
	
	def predict(self, X):
		self.predicted_y = self.clf.predict(X)
		return self.predicted_y

	def score(self, X, y, weight = None):
		return self.clf.score(X, y, weight)