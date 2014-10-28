"""
	util.py
	File contains utilities
"""

import sys, os, json
data_directory = 'data' # directory that all data is stored in

def load_data(source_file = 'amazon_review_test.txt'):
	print "loading data..."
	data_pathname = os.path.join(data_directory, source_file)
	with open(data_pathname, 'r+') as f:
		dataset = [json.loads(line) for line in f]
	print 'finished reading json'
	return dataset