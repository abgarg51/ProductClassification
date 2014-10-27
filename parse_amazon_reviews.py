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

def getListOfNodeIDForRootParent(rootParentName):
	nodeIds = {}
	with open('./data/AmazonHeirarchy.json', 'r+') as data:
		jsons = []
		for line in data:
			jsonObj = json.loads(line)
			jsons.append(jsonObj)
		

		def getChildren(subTree):
			nodeIds[subTree['BrowseNodeId']] = subTree['Name']
			if not subTree.has_key('Children'):
				#print "No children for: ", subTree
				return
			children = subTree['Children']
			if type(children) is not list:
				children = [children]
			for child in children:
				if type(child) is dict:
					getChildren(child)
			return children

		for tree in jsons[0]:
			if tree['Name'] == rootParentName:
				nodeIds[tree['BrowseNodeId']] = tree['Name']
				for child in tree['Children']:
					getChildren(child)
	return nodeIds



#####  MAIN  #######	

outFile = io.open("./data/amazon_review.txt", "w", encoding='utf-8')

with open('./data/amazon_products', 'r+') as data_file:
	jsons = []
	appliancesNodeIds = getListOfNodeIDForRootParent('Appliances')
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
		for nodeID in browseNodeIDs:
			if nodeID not in appliancesNodeIds.keys():
				browseNodeIDs.remove(nodeID)
		if len(browseNodeIDs) > 0:
			applianceCount += 1
		for text in reviewTexts:
			reviewCount += 1
			for ID in browseNodeIDs:
				out_obj = {'review':text, 'id':ID}
				outFile.write(unicode(json.dumps(out_obj, ensure_ascii=False)))
				outFile.write(unicode('\n'))

print "Processed ", productCount, " products, with ", reviewCount, "reviews, ", applianceCount, "of products are appliances and exported."
print "content exported to ./data/amazon_review.txt"