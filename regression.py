from sklearn import linear_model, datasets
import pandas as pd
from featureExtractor import extractFeatures
import json
import numpy as np

with open('data/amazon_review_test.txt', 'r') as f :
    dataset = [json.loads(line) for line in f]
    
reviews = [d['review'] for d in dataset]
features = [dict(extractFeatures(r)) for r in reviews]
X = pd.DataFrame(features).fillna(0)
y = [d['id'] for d in dataset]

clf = linear_model.LogisticRegression()
clf.fit(X, y)
predicted_y = clf.predict(X)
print "Prediction success rate = %.4f"%(sum(predicted_y == y)*1./len(y))