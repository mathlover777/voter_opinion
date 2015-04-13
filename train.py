# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/abir/mosek/7/tools/platform/linux64x86/bin/

import config
import datahandler
import createmle as ML
import solveconcave as SC
import utility as UTIL
import extractsolutions

def reportFailure(nodeId,influencesbyId,expressionList,exceptionString = '',stringFlag = False):
	with open(config.failureLog, "a") as myfile:
		myfile.write('***************************************** [node = ' + str(nodeId) + ']\n')
		if(not stringFlag):
			myfile.write(str(influencesbyId))
			myfile.write('\n')
			myfile.write(str(expressionList))
			myfile.write('\n')
		else:
			myfile.write(exceptionString + '\n')

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
			exceptionString = ''
			stringFlag = False
			if(len(influencesbyId) > 0):
				# other wise its not an exception as its a lonely node
				failCount = failCount + 1
			else:
				exceptionString = 'Lonely node'
				stringFlag = True
			reportFailure(nodeId,influencesbyId,expressionList,exceptionString,stringFlag)
			A = A + [extractsolutions.getDefaultWeights(D,nodeId,nodeIdToCurrentIndex)]
		done = done + 1
		UTIL.drawProgressBar(float(done)/float(len(nodeList)),'failCount = ' + str(failCount) + '/' + str(done), 50)
	UTIL.saveDictionaryAsJson(A,config.adjacencyName)

def resetLogger():
	with open(config.failureLog, "w+") as f:
		print 'log reset done'
def main():
	resetLogger()
	computeAndSaveA(config.timestamp)
if __name__ == "__main__": main()