import json
import io

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

def getCatgoryDictForRootParent(rootParentName):
	nodeIds = {}
	nodeIdToCatgoryDict = {}
	catogoryIdToNameDict = {}
	conflicts = []
	with open('./data/AmazonHeirarchy.json', 'r+') as data:
		jsons = []
		for line in data:
			jsonObj = json.loads(line)
			jsons.append(jsonObj)
		

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

		for tree in jsons[0]:
			if tree['Name'] == rootParentName:
				nodeID = int(tree['BrowseNodeId']) 
				nodeIds[nodeID] = tree['Name']
				nodeIdToCatgoryDict[nodeID] = nodeID
				for child in tree['Children']:
					catId = child['BrowseNodeId']
					catName = child['Name']
					catogoryIdToNameDict[catId] = catName
					getChildren(child, catId)

		#print catogoryIdToNameDict
		#print nodeIds
		#print nodeIdToCatgoryDict
		print "nodeID count in dict: ", len(nodeIdToCatgoryDict)
		print "nodeID count in list: ", len(nodeIds)
		#print "Conflicts: ========================"
		#for conflict in conflicts:
		#	print "Conflict: (NodeID, new catgoryID, old category ID) = ", conflict
		for nodeID in nodeIds:
			if (not nodeIdToCatgoryDict.has_key):
				print "Missing nodeID from dict: ",nodeID
	return nodeIdToCatgoryDict



#####  MAIN  #######	

outFile = io.open("./data/amazon_review.txt", "w", encoding='utf-8')

with open('./data/amazon_products', 'r+') as data_file:
	jsons = []
	nodeIdToCatgoryDict = getCatgoryDictForRootParent('Appliances')
	productCount = 0
	reviewCount = 0
	applianceCount = 0
	for line in data_file:
		try:
			item = json.loads(line.strip()[:-1])
		except ValueError, e:
			print "Format error"
			continue
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
		#skip if no ID is left
		if len(browseNodeIDs) > 0:
			applianceCount += 1
		else:
			continue
		#start to print
		for text in reviewTexts:
			reviewCount += 1
			for ID in browseNodeIDs:
				#put in catogory ID instead of the browsnodeID of the node.
				out_obj = {'review':text, 'id':nodeIdToCatgoryDict[ID]}
				outFile.write(unicode(json.dumps(out_obj, ensure_ascii=False)))
				outFile.write(unicode('\n'))

print "Processed ", productCount, " products, with ", reviewCount, "reviews, ", applianceCount, "of products are appliances and exported."
print "content exported to ./data/amazon_review.txt"