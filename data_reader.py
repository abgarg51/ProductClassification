import json
import io
import sys
from collections import Counter

######################################
# How to use:
# Put unziped amazon_products and AmazonHeirarchy.json under ./data, then run this script without
# output file will be ./data/amazon_review.txt
# output format is:
# each line is a json object, contains a dict with key "review" for the review text, and "id" for the BrowseNodeId
#
# Note: amazon_products or the output file are too large to upload to github.
# Warning: the script is silentlly discarding mis-formated Items.
######################################

def getCatgoryDictForRootParent(trees,rootParentName):
	nodeIds = {}
	nodeIdToCatgoryDict = {}
	catogoryIdToNameDict = {}
	conflicts = []
	#recursive sub routine to search down the tree.
	def getChildren(subTree, catId):
		nodeID = int(subTree['BrowseNodeId']) 
		nodeIds[nodeID] = subTree['Name']
		if (nodeIdToCatgoryDict.has_key(nodeID) and (nodeIdToCatgoryDict[nodeID] != catId)):
			conflicts.append((nodeID, catId, nodeIdToCatgoryDict[nodeID]))
		else:
			nodeIdToCatgoryDict[nodeID] = catId
		if not subTree.has_key('Children'):
			#print "No children for: ", subTree
			return
		children = subTree['Children']
		if type(children) is not list:
			children = [children]
		for child in children:
			if type(child) is dict:
				getChildren(child, catId)
		return children
			
		#start from the root, use first level children as rollup catagories.
	for tree in trees:
		if tree['Name'] == rootParentName:
			nodeID = int(tree['BrowseNodeId']) 
			nodeIds[nodeID] = tree['Name']
			nodeIdToCatgoryDict[nodeID] = nodeID
			for child in tree['Children']:
				catId = child['BrowseNodeId']
				catName = child['Name']
				catogoryIdToNameDict[catId] = catName
				getChildren(child, catId)

	print "CategoryID to Name mapping FYI:"
	print catogoryIdToNameDict
	#print nodeIds
	#print nodeIdToCatgoryDict
	print "nodeID count in dict: ", len(nodeIdToCatgoryDict)
	#print "nodeID count in list: ", len(nodeIds)
	#print "Conflicts: ========================"
	#for conflict in conflicts:
	#	print "Conflict: (NodeID, new catgoryID, old category ID) = ", conflict
	for nodeID in nodeIds:
		if (not nodeIdToCatgoryDict.has_key):
			print "Missing nodeID from dict: ",nodeID
	return nodeIdToCatgoryDict


def getRootCatgoryNames(amazoneTrees):
	rootCatgoryNames = []
	for tree in amazoneTrees:
		rootCatgoryNames.append(tree['Name'])
	return rootCatgoryNames

def printRootCatgoryNames(rootCatgoryNames):
	for i in range(len(rootCatgoryNames)):
		print "Index: ",i, "\t",rootCatgoryNames[i]


def loadAmazoneHeirarchyTree(treeName):
	with open(treeName, 'r+') as data:
		jsons = []
		for line in data:
			jsonObj = json.loads(line)
			jsons.append(jsonObj)
		amazoneTrees = jsons[0]
	return amazoneTrees



def parseAmazonDataWithNodeIDDict(rawDataFileName,nodeIdToCatgoryDict,ouputFileName,numLimit):
	outFile = io.open(ouputFileName, "w", encoding='utf-8')
	with open(rawDataFileName, 'r+') as data_file:
		productCount = 0
		reviewCount = 0
		matchingProdCount = 0
		progressPrintCount = 0
		for line in data_file:
			try:
				item = json.loads(line.strip()[:-1])
			except ValueError, e:
				print "Format error"
				continue
	
			#print a dot for each 100 line of data file.
			progressPrintCount += 1
			if progressPrintCount == 100:
				print '.',
				sys.stdout.flush()
				progressPrintCount = 0
			
			reviews = item['Item']['PrunedReivews'];
			reviewTexts = [rev['Content'] for rev in reviews]
			if not item['Item'].has_key('BrowseNodes'):
				continue
			productCount += 1
			browseNodes = item['Item']['BrowseNodes']['BrowseNode']
			if type(browseNodes) is not list:
				browseNodes = [browseNodes]
			browseNodeIDs = [node['BrowseNodeId'] for node in browseNodes if node.has_key('BrowseNodeId')]
			#filter out none appliance IDs.
			browseNodeIDs = [node for node in browseNodeIDs if node in nodeIdToCatgoryDict.keys()]
			categoryIDs = Counter()
			#skip if no ID is left
			if len(browseNodeIDs) > 0:
				matchingProdCount += 1
			else:
				continue
			for nodeID in browseNodeIDs:
				categoryIDs[nodeIdToCatgoryDict[nodeID]] += 1
			categoryIDMaxMatch = max(categoryIDs, key=categoryIDs.get)

			#start to print
			for text in reviewTexts:
				reviewCount += 1
				#put in catogory ID instead of the browsnodeID of the node.
				out_obj = {'review':text, 'id':categoryIDMaxMatch}
				outFile.write(unicode(json.dumps(out_obj, ensure_ascii=False)))
				outFile.write(unicode('\n'))

			#break loop if limits are reached
			if matchingProdCount >= numLimit:
				break
	print ""
	print "Processed ", productCount, " products, with ", reviewCount, "reviews, ", matchingProdCount, "of products are match and exported."
	print "content exported to:", ouputFileName

def parseSocialDataWithNodeIDDict(channelName, inputFileName, nodeIdToCatgoryDict, outFileName, outputLineCountLimit):
	outFile = io.open(outFileName, "w", encoding='utf-8')
	with open(inputFileName, 'r+') as data_file:
		matchingProdCount = 0
		progressPrintCount = 0
		textCount = 0
		for line in data_file:
			textCount += 1
			try:
				item = json.loads(line.strip())
			except ValueError, e:
				print "Format error"
				continue

			#print a dot for each 100 line of data file.
			progressPrintCount += 1
			if progressPrintCount == 100:
				print '.',
				sys.stdout.flush()
				progressPrintCount = 0

			if item['conversation_src'] != channelName:
				if item['conversation_src'] not in ['ebay', 'tw']:
					print "Unkown channel name: ", item['conversation_src']
				continue

			browseNodes = item['Amazon_Browsenodes']
			text = item['conversation_text']
			browseNodeIDs = []
			categoryIDs = Counter()

			if item['conversation_src'] == 'tw':
				browseNodes = browseNodes['BrowseNode']
				
			if type(browseNodes) == list:
				for browseNode in browseNodes:
					#print browseNode
					browseNodeId = browseNode['BrowseNodeId']
					browseNodeIDs.append(browseNodeId)
				
			elif type(browseNodes) == dict:
				browseNodeId = browseNodes['BrowseNodeId']
				browseNodeIDs.append(browseNodeId)
			else:
				print "Error, unexpected browseNodes type: ", type(browseNodes)
			browseNodeIDs = [node for node in browseNodeIDs if node in nodeIdToCatgoryDict.keys()]
			if len(browseNodeIDs) == 0:
				continue
			for nodeID in browseNodeIDs:
				categoryIDs[nodeIdToCatgoryDict[nodeID]] += 1
			categoryIDMaxMatch = max(categoryIDs, key=categoryIDs.get)

			#TODO: add check before adding it as match.
			matchingProdCount += 1

			#put in catogory ID instead of the browsnodeID of the node.
			out_obj = {'review':text, 'id':categoryIDMaxMatch}
			outFile.write(unicode(json.dumps(out_obj, ensure_ascii=False)))
			outFile.write(unicode('\n'))

			if matchingProdCount >= outputLineCountLimit:
				break
	print ""
	print "Processed ", textCount, " texts, from channel ", channelName, ", ", matchingProdCount, "of them are match and exported."
	print "content exported to:", outFileName



#####  MAIN  #######

if __name__ == "__main__":
	channels = ['amazon','twitter', 'ebay']
	amazoneTrees = loadAmazoneHeirarchyTree('./data/AmazonHeirarchy.json')
	rootCatgoryNames = getRootCatgoryNames(amazoneTrees)

	#evaluating arguments:
	if ((len(sys.argv) != 4 and len(sys.argv) != 5) or sys.argv[1] not in channels):
		print "Example: data_reader.py amazon 2 ./data/amazone_art.txt"
		print "Or:      data_reader.py twitter 2 ./data/twitter_app.txt 200"
		print "1st argument is the data source in one of these: [amazon,twitter, ebay]"
		print "2nd argument is the catogoryID as in following list"
		print "3rd argument is the output file name"
		print "4th argument is optional, and can be used to limit number of products processed"
		printRootCatgoryNames(rootCatgoryNames)
		exit()

	channel = sys.argv[1]
	selectedCatIndex = int(sys.argv[2])
	if (selectedCatIndex < 0 or selectedCatIndex > len(rootCatgoryNames)-1):
		print "Catogory Index out of range: 1-",len(rootCatgoryNames)-1
		exit()
	else:
		category = rootCatgoryNames[selectedCatIndex]
		print "Filtering with catogory: ", category

	outFileName = sys.argv[3]

	if len(sys.argv) == 5:
		outputLineCountLimit = int(sys.argv[4])
		print "With output line count limit: ", outputLineCountLimit
	else:	
		outputLineCountLimit = float("inf")
	#finished evaluating arguments
	
	#Start working:	
	nodeIdToCatgoryDict = getCatgoryDictForRootParent(amazoneTrees, category)

	if (channel == 'amazon'):
		parseAmazonDataWithNodeIDDict('./data/amazon_products.dat', nodeIdToCatgoryDict, outFileName, outputLineCountLimit)
	elif(channel == 'ebay'):
		print "Processing eBay data."
		parseSocialDataWithNodeIDDict('ebay','./data/Social_Conversations_AmazonLabel.json.dat', nodeIdToCatgoryDict, outFileName, outputLineCountLimit)
	elif(channel == 'twitter'):
		parseSocialDataWithNodeIDDict('tw','./data/Social_Conversations_AmazonLabel.json.dat', nodeIdToCatgoryDict, outFileName, outputLineCountLimit)
		print "Processing twitter"
	else:
		#should not get here anyway....
		print "Invalid channel name: ", channel

