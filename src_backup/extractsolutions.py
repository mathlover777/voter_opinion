def extractAdjacecnyWeights(D,nodeId,solution,nodeIdToCurrentIndex):
	A = {}
	totalExternalBias = 0.0
	for currentnodeId in nodeIdToCurrentIndex:
		currentIndex = nodeIdToCurrentIndex[currentnodeId]
		A[currentnodeId] = solution[currentIndex]
		totalExternalBias = totalExternalBias + solution[currentIndex]
	if nodeId not in A:
		A[nodeId] = 1.0 - totalExternalBias
	return A
def getDefaultWeights(D,nodeId,nodeIdToCurrentIndex):
	# print nodeIdToCurrentIndex
	A = {}
	if nodeId not in A:
		influenceCount = float(len(nodeIdToCurrentIndex) + 1)
		A[nodeId] = 1.0 / influenceCount
	else:
		influenceCount = float(len(nodeIdToCurrentIndex))
	weight = 1.0 / influenceCount
	for currentnodeId in nodeIdToCurrentIndex:
		A[currentnodeId] = weight
	return A