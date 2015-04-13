# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/abir/mosek/7/tools/platform/linux64x86/bin/

import config
import datahandler
import createmle as ML
import solveconcave as SC
import utility as UTIL
import extractsolutions

def computeAndSaveA(timeStamp,nodeList = None):
	D = datahandler.Datahandler(config.datasetName)
	if nodeList == None:
		nodeList = D.getNodeList()
	done = 0
	A = []
	failCount = 0
	for nodeId in nodeList:
		((influencesbyId,expressionList),nodeIdToCurrentIndex) = ML.setProblemByNodeId(D,timeStamp,nodeId)
		try:
			solution = SC.solveConcave(influencesbyId,expressionList)
			A = A + [extractsolutions.extractAdjacecnyWeights(D,nodeId,solution,nodeIdToCurrentIndex)]
		except:
			failCount = failCount + 1
			A = A + [extractsolutions.getDefaultWeights(D,nodeId,nodeIdToCurrentIndex)]
		done = done + 1
		UTIL.drawProgressBar(float(done)/float(len(nodeList)),'failCount = ' + str(failCount) + '/' + str(done), 50)
	UTIL.saveDictionaryAsJson(A,config.adjacencyName)

def main():
	computeAndSaveA(config.timestamp)
if __name__ == "__main__": main()