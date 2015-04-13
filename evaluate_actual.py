import config
import utility
import random
import datahandler


def nextOpinion(D,currentNodeId,lastOpinionOfCurrentNode,adjacency,time):
	influenceOpinions = D.getDiscreteInfluenceOpinionsById(time, currentNodeId)
	transProb = 0.0
	for (influenceNode, influenceOpinion) in influenceOpinions:
		if(influenceOpinion != lastOpinionOfCurrentNode):
			# will participate in influence
			transProb += adjacency[currentNodeId][str(influenceNode)]			
		else:
			# will not participate in influence
			pass

	# If transition prob is greate than 0.5 then flip, else don't
	if transProb>0.5 :
		return 1-lastOpinionOfCurrentNode

	return lastOpinionOfCurrentNode

def calculateCase1Actual(D, adjacency):


	traindeTillTime = config.timestamp
	nodeList = D.getNodeList()


	print "***********case1 : using last original ************"
	Result = {}
	totalAccuracy = 0.0
	actualCount = 0
	for node in nodeList:
		actualOpinions = D.getAllDiscreteOpinionOnorAfterTimeById(traindeTillTime,node)
		influences = D.getInfluencesById(node)

		total_opinions = 0
		opinions_matched = 0
		for (time, opinion) in actualOpinions:
			
			lastOpinionOfCurrentNode = D.getDiscreteOpinionBeforeTimeById(time, node)
			new_opinion = nextOpinion(D, node, lastOpinionOfCurrentNode, adjacency, time)

			if new_opinion == opinion:
				opinions_matched += 1
			total_opinions += 1

		if total_opinions == 0:
			continue
		matchPercent = (float(opinions_matched)/float(total_opinions))*100.0

		Result[node] = str(matchPercent) + " " + str(opinions_matched) + "/" + str(total_opinions)
		totalAccuracy = totalAccuracy + matchPercent
		actualCount = actualCount + 1

	utility.saveAsJson(Result,config.resultFile_pernode_using_lastOriginal)
	print ("For out of " + str(actualCount) + "/" + str(len(nodeList)) + " Average Accuracy = " + str(totalAccuracy /float(actualCount)))
	return Result
		

def calculateCase2Actual(D, adjacency):


	traindeTillTime = config.timestamp
	nodeList = D.getNodeList()


	print "***********case2: using always predicted ************"
	Result = {}
	totalAccuracy = 0.0
	actualCount = 0
	for node in nodeList:
		actualOpinions = D.getAllDiscreteOpinionOnorAfterTimeById(traindeTillTime,node)
		influences = D.getInfluencesById(node)

		total_opinions = 0
		opinions_matched = 0

		if len(actualOpinions) == 0:
			continue

		lastOpinionOfCurrentNode = D.getDiscreteOpinionBeforeTimeById(actualOpinions[0][0], node)

		for (time, opinion) in actualOpinions:
			
			# lastOpinionOfCurrentNode = D.getDiscreteOpinionBeforeTimeById(time, node)
			new_opinion = nextOpinion(D, node, lastOpinionOfCurrentNode, adjacency, time)

			if new_opinion == opinion:
				opinions_matched += 1
			total_opinions += 1

			lastOpinionOfCurrentNode = new_opinion

		if total_opinions == 0:
			continue
		matchPercent = (float(opinions_matched)/float(total_opinions))*100.0

		Result[node] = str(matchPercent) + " " + str(opinions_matched) + "/" + str(total_opinions)
		totalAccuracy = totalAccuracy + matchPercent
		actualCount = actualCount + 1

	utility.saveAsJson(Result,config.resultFile_pernode_using_lastPredicted)
	print ("For out of " + str(actualCount) + "/" + str(len(nodeList)) + " Average Accuracy = " + str(totalAccuracy /float(actualCount)))
	return Result

def evaluate():

	D = datahandler.Datahandler(config.datasetName)
	
	learnedAdjacency = utility.loadJsonObject(config.adjacencyName)
	calculateCase1Actual(D, learnedAdjacency)
	calculateCase2Actual(D, learnedAdjacency)

def main():
	evaluate()
	
if __name__ == "__main__":
	main()
