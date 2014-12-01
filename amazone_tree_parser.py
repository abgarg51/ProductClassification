import json
import io
import sys
from collections import Counter

def loadAmazoneHeirarchyTree(treeName):
	with open(treeName, 'r+') as data:
		jsons = []
		for line in data:
			jsonObj = json.loads(line)
			jsons.append(jsonObj)
		amazoneTrees = jsons[0]
	return amazoneTrees



def getRootCatgoryNames(amazoneTrees):
	rootCatgoryNames = []
	for tree in amazoneTrees:
		rootCatgoryNames.append(tree['Name'])
	return rootCatgoryNames

def printRootCatgoryNames(rootCatgoryNames):
	for i in range(len(rootCatgoryNames)):
		print "Index: ",i, "\t",rootCatgoryNames[i]

def getCatgoryNamesForRootParent(trees,rootParentName):
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
			if not tree.has_key('Children'):
				continue
			for child in tree['Children']:
				catId = child['BrowseNodeId']
				catName = child['Name']
				catogoryIdToNameDict[catId] = catName
				getChildren(child, catId)

	#print "CategoryID to Name mapping FYI:"
	#print catogoryIdToNameDict
	#print nodeIds
	#print nodeIdToCatgoryDict
	#print "nodeID count in dict: ", len(nodeIdToCatgoryDict)
	#print "nodeID count in list: ", len(nodeIds)
	#print "Conflicts: ========================"
	#for conflict in conflicts:
	#	print "Conflict: (NodeID, new catgoryID, old category ID) = ", conflict
	for nodeID in nodeIds:
		if (not nodeIdToCatgoryDict.has_key):
			print "Missing nodeID from dict: ",nodeID
	return catogoryIdToNameDict

if __name__ == "__main__":
	amazoneTrees = loadAmazoneHeirarchyTree('./data/AmazonHeirarchy.json')
	ouputFileName = "./data/amazonCategoryNames.txt"
	scratchFileName = "./scratch/amazon_category_names.txt"
	scratchCSVFileName = "./scratch/amazon_category_names.csv"
	rootCatgoryNames = getRootCatgoryNames(amazoneTrees)
	outFile = io.open(ouputFileName, "w", encoding='utf-8')
	scratchFile = io.open(scratchFileName, "w")
	csvFile = io.open(scratchCSVFileName, "w")

	outputDict = {}

	for cat in rootCatgoryNames:
		names = getCatgoryNamesForRootParent(amazoneTrees, cat)
		outputDict[cat] = names
		for name in names.keys():
			scratchText =  u' '.join((cat, " --> " , name , " --> " , names[name])).encode('utf-8').strip()
			csvText = u' '.join((name , "," , names[name])).encode('utf-8').strip()
			#cat + " --> " + name + " --> " + names[name].encode('utf-8').strip()
			print scratchText
			scratchFile.write(unicode(scratchText, errors='ignore')+'\n')
			csvFile.write(unicode(csvText, errors='ignore')+'\n')


	outFile.write(unicode(json.dumps(outputDict, ensure_ascii=False)))
	#outFile.write(unicode('\n'))

	print "amazone category information exported to: ", ouputFileName, " as Json dict."
	print "Format:"
	print "it's a Json of a dict, keys are root category names. Value is another Dict."
	print "Value dict has catgoryID as keys, and names as values"
	print "==========================================================================="
	print "Also exported to ", scratchFileName, "with txt format"

	#print outputDict


