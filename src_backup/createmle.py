import pprint

def setProblemByNodeId(D,timestamp,nodeId):
	# checkSanity(D,timestamp,nodeId)

	influences = D.getInfluencesById(nodeId)

	trainOpinions = D.getAllDiscreteOpinionBeforeTimeById(timestamp,nodeId)

	# print 'influences :',influences
	# print 'train Opinions :',trainOpinions

	if (trainOpinions < 2):
		print "not enough data to train !!"
		quit()

	(prevTimestamp,prevOpinion) = trainOpinions[0]
	trainOpinions.pop(0)

	# log (a1x1 + a2x2 + ... anxn + c)
	# is stored in array as
	# ([(i1,ai1),(i2ai2),...,(ik,aik)],c)

	nodeCount = float(D.getNodeCount())

	# print nodeCount,(prevTimestamp,prevOpinion),trainOpinions
	expressionList = []

	nodeIdToCurrentIndex = {}
	i = 0
	for node in influences:
		nodeIdToCurrentIndex[node] = i
		i = i + 1

	for (cTime,cOpinion) in trainOpinions:
		transionRequired = True
		if(prevOpinion == cOpinion):
			transionRequired = False
		(prevTimestamp,prevOpinion) = (cTime,cOpinion)
		# print 'transionRequired :',transionRequired
		previousInfluenceOpinions = D.getDiscreteInfluenceOpinionsById(cTime,nodeId)
		# print 'Real:',previousInfluenceOpinions
		prevValidInfluenceOpinions = filter(lambda (node,opinion): opinion != None,previousInfluenceOpinions)
		# print 'Cleaned:',prevValidInfluenceOpinions
		prevDifferentInfluences = filter(lambda (node,opinion): opinion!= cOpinion,prevValidInfluenceOpinions)
		# print 'cOpinion :',cOpinion,' Different:',prevDifferentInfluences
		indexedInfluenceOpinions = map(lambda (nodeId,opinion):(nodeIdToCurrentIndex[nodeId],opinion),prevDifferentInfluences)
		# print 'transion',transionRequired,'Indexed :',indexedInfluenceOpinions
		coefficients = map(lambda (nodeCurrentIndex,opinion): (nodeCurrentIndex,1.0/nodeCount) if (transionRequired) else (nodeCurrentIndex,-1.0/nodeCount),indexedInfluenceOpinions)

		# print 'coefficients:',coefficients
		sparseCoefficients = filter(lambda (index,coefficient):coefficient != 0.0,coefficients)
		# print 'sparse :',sparseCoefficients
		constantTerm = 0.0
		if(transionRequired):
			constantTerm = 0.0
		else:
			constantTerm = 1.0

		expression = (sparseCoefficients,constantTerm)
		# print 'expression',expression
		expressionList = expressionList + [expression]

	# print 'Objective parts'
	# print expressionList

	influencesbyId = [nodeIdToCurrentIndex[x] for x in influences]


	# print 'constraints'
	# print influencesbyId

	return ((influencesbyId,expressionList),nodeIdToCurrentIndex)

def test(D):
	pprint.pprint( setProblemByNodeId(D,1355750721,29))
	return