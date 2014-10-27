# simple example to do multi class logistic regression

import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model, datasets
import pandas as pd

# import some data to play with
iris = datasets.load_iris()
X = iris.data[:, :2]  # we only take the first two features.
Y = pd.Series(iris.target)

logreg = linear_model.LogisticRegression(C=1e5)
logreg.fit(X, Y)

print logreg.predict((1,2))
