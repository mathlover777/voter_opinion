import config
import string
import utility

def createIDmapping(nodeListFile):
	nodeList = map(lambda nodeString: int(nodeString), file(nodeListFile).readlines())
	nodeIdToIndex = {}
	nodeIndexToId = []
	i = 0
	for node in nodeList:
		nodeIdToIndex[node] = i
		nodeIndexToId = nodeIndexToId + [node]
		i = i + 1
	return (nodeIdToIndex,nodeIndexToId)

def create_nodeList_clean(idmap,inputfile,outputfile):
	nodeCount = len(idmap)
	outputHandler = open(outputfile,"w")
	nodeList = map(lambda nodeIndex: str(nodeIndex) + '\n',range(nodeCount))
	outputHandler.writelines(nodeList)


def create_edgeList_clean(idmap,inputfile,outputfile):
	inputhandler = file(inputfile)
	outputHandler = open(outputfile,"w")

	dirty_edgeList = map(lambda (a,b):(int(a),int(b)),map(lambda l:string.split(l),inputhandler.readlines()))
	clean_edgeList = map(lambda (a,b):str(idmap[a]) + ' ' + str(idmap[b]) + '\n',dirty_edgeList)
	outputHandler.writelines(clean_edgeList)

def create_post_clean(idmap,inputfile,outputfile):
	inputhandler = file(inputfile)
	outputHandler = open(outputfile,"w")

	clean_postList = map(lambda x:str(idmap[int(x[0])]) + ' ' + string.join(x[1:]) + '\n',map(lambda l:string.split(l),inputhandler.readlines()))

	# print clean_postList
	outputHandler.writelines(clean_postList)

def main():
	nodeListFile = config.datasetName + config.nodeListFile
	edgeListFile = config.datasetName + config.edgeListFile
	postFile = config.datasetName + config.postFile

	nodeListFile_clean = config.datasetName + config.nodeListFile_clean
	edgeListFile_clean = config.datasetName + config.edgeListFile_clean
	postFile_clean = config.datasetName + config.postFile_clean

	nodeIdToIndexMap = config.datasetName + config.nodeIdToIndexMap
	nodeIndexToIdMap = config.datasetName + config.nodeIndexToIdMap
	
	(nodeIdToIndex,nodeIndexToId) = createIDmapping(nodeListFile)
	create_nodeList_clean(nodeIdToIndex,nodeListFile,nodeListFile_clean)
	create_edgeList_clean(nodeIdToIndex,edgeListFile,edgeListFile_clean)
	create_post_clean(nodeIdToIndex,postFile,postFile_clean)

	utility.saveAsJson(nodeIdToIndex,nodeIdToIndexMap)
	utility.saveAsJson(nodeIndexToId,nodeIndexToIdMap)
	
	# print nodeIdToIndex
	# print nodeIndexToId

if __name__ == "__main__": main()