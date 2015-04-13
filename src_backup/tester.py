import datahandler
import utility
import config
import createmle as CM
import analyze as AN
import solveconcave as SC
import utility as UTIL
import extractsolutions

#################### TEST AND ANALYSIS #####################################
def analyze():
	D = datahandler.Datahandler(config.datasetName)
	CM.test(D)
	AN.analyzeDataset(D)
	minGoodTime = AN.analyzeTimeData(D)
	AN.plotScatter(D,minGoodTime)
	AN.findAllLonelyNodes(D)
	print minGoodTime

def test():
	D = datahandler.Datahandler(config.datasetName)

	################# testing the main problem ######################################
	nodeId = 29
	timeStamp = 1355750721
	((influencesbyId,expressionList),nodeIdToCurrentIndex) = CM.setProblemByNodeId(D,timeStamp,nodeId)
	# print nodeIdToCurrentIndex
	# print currentIndexToNodeId
	solution = SC.solveConcave(influencesbyId,expressionList)
	# print solution

	A = extractsolutions.extractAdjacecnyWeights(D,nodeId,solution,nodeIdToCurrentIndex)
	print A
def solverTest():
	# all positive tests
	# test 1# passed
	# solution = SC.solveConcave([0,1],[([(0,1.0)],0),([(1,1.0)],0)])
	# test 2 # passed
	# solution = SC.solveConcave([0,1,2,3],[([(0,1.0)],0),([(1,1.0)],0),([(2,1.0)],0),([(3,1.0)],0)])
	# test 3 #passed 
	# solution = SC.solveConcave([0,1,2,3],[([(0,1.0),(1,1.0)],0),([(1,1.0)],0),([(2,1.0)],0),([(3,1.0)],0)])
	# test 4  #passed
	# solution = SC.solveConcave([0,1,2,3],[([(0,1.0),(1,1.0)],0),([(0,1.0),(1,1.0),(2,1.0)],0),([(2,1.0)],0),([(3,1.0)],0)])
	# test 5 #passed
	# solution = SC.solveConcave([0,1,2,3],[([(0,-1.0),(1,-1.0)],1.0),([(0,1.0),(1,1.0),(2,1.0)],0),([(2,1.0)],0),([(3,1.0)],0)])
	# test 6 #passed
	# solution = SC.solveConcave([0,1,2,3],[([(0,-1.0),(1,-1.0)],1.0),([(0,-1.0),(1,-1.0),(2,-1.0)],1.0),([(2,1.0)],0),([(3,1.0)],0)]) #passed
	# solution = SC.solveConcave([0,1,2,3],[([(0,-1.0),(1,-1.0)],1.0),([(0,-1.0),(1,-1.0),(2,-1.0)],1.0),([(2,1.0),(3,1.0)],0)])
	# test 7 # passed
	# solution = SC.solveConcave([0,1,2],[([(0,1.0)],0),([(1,2.0)],0),([(2,-1.0)],1.0)])
	# solution = SC.solveConcave([0,1,2],[([(0,1.0)],0),([(1,2.0)],0),([(2,-0.5)],1.0)])
	# solution = SC.solveConcave([0,1,2],[([(0,.6)],0),([(1,.1)],0),([(2,-0.5)],1.0)])
	# solution = SC.solveConcave([0,1,2],[([(0,.6),(1,.3)],0),([(1,.1)],0),([(2,-0.05)],1.0)])
	# passed [1.1432205021224266e-09, 6.183828690348964e-10, 0.999999997607273]
	# solution = SC.solveConcave([0,1,2],[([(0,0.6),(2,0.3)],0),([(1,0.1),(2,1.0)],0),([(2,-0.05),(0,-1.0),(1,-1.0)],1.0)])
	# passed [6.468583698913718e-10, 1.1803945238846308e-09, 0.9999999893772406]
	# minimize (-log(1-0.6x - 0.3z)-log(0.1y+z) -log(1-0.05z-x-y)) over 0<=1.0x+1y+1.0z<=1, 0<=x<=1, 0<=y<=1, 0<=z<=1
	# solution = SC.solveConcave([0,1,2],[([(0,-0.6),(2,-0.3)],1.0),([(1,0.1),(2,1.0)],0),([(2,-0.05),(0,-1.0),(1,-1.0)],1.0)])
	# solution = SC.solveConcave([0,1,2],[([(0,1.0),(1,1.0)],0.0),([(1,1.0),(2,1.0)],0.0),([(2,1.0),(0,1.0)],0.0)])
	solution = SC.solveConcave([0,1,2],[([(0,2.0),(1,3.0)],0.0),([(1,3.0),(2,5.0)],0.0),([(2,1.0),(0,2.0)],0.0)])
	print solution
	print 'mosek tested'
############################################################################
def testDataHandler():
	D = datahandler.Datahandler(config.datasetName)
	D.saveAsJson()
	# print 'here'
def main():
	test()
	# analyze()
	# solverTest()
	# computeAndSaveA(1355750721,[4221,14062])
	# testDataHandler()

if __name__ == "__main__": main()