import config
import utility
import random
import datahandler

def getNewOpinion(D,opinionVector,adjacency,nodeId):
	transprob = 0.0
	currentOpinion = opinionVector[nodeId]
	# print adjacency[nodeId]
	for influence in D.getInfluencesById(nodeId):
		if(currentOpinion != opinionVector[influence]):
			transprob = transprob + adjacency[nodeId][str(influence)]
		else:
			pass

	random_float = random.random()
	if(random_float <= transprob):
		return (1-currentOpinion)
	else:
		return currentOpinion


def getNewOpinionList(D,opinionVector,adjacency):
	nodeCount = len(opinionVector)
	newopinionVector = map(lambda nodeId:getNewOpinion(D,opinionVector,adjacency,nodeId) ,range(0,len(opinionVector)))
	return newopinionVector

def simulate(D,adjacency,simulationStartTime):
	opinionList = map(lambda nodeid:D.getDiscreteOpinionBeforeTimeById(simulationStartTime,nodeid),D.getNodeList())
	lastTime = D.getTimeStampCount()
	successCount = 0
	totalTestCount = 0
	for timestamp in xrange(simulationStartTime,lastTime+1):
		# for each time after train
		opinionList = getNewOpinionList(D,opinionList,adjacency) # predicted opinions for this time instance
		observeredOpinions = D.getOpinionsForAllNodesIfAvailable(timestamp)
		# print observeredOpinions
		if(len(observeredOpinions) == 0):
			continue
		for nodeId in observeredOpinions:
			opinion = observeredOpinions[nodeId]
			totalTestCount = totalTestCount + 1
			if(opinion == opinionList[nodeId]):
				successCount = successCount + 1
			else:
				pass

	if(totalTestCount == 0):
		print 'no observation to test'
		return 0.0
	print('out of ' + str(totalTestCount) + ' success = ' + str(successCount))
	accuracy = float(successCount) / float(totalTestCount)
	print('accuracy = ' + str(accuracy))

	return accuracy

def main():
	# config.init_config()
	D = datahandler.Datahandler(config.datasetName)
	# print config.adjacencyName
	learnedAdjacency = utility.loadJsonObject(config.adjacencyName)
	simulate(D,learnedAdjacency,config.timestamp)

if __name__ == "__main__":
	main()