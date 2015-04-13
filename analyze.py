import matplotlib.pyplot as plt
import config
import string
from collections import Counter

def analyzeDataset(D):
	nodeList = D.getNodeList()
	opinionStatDict = {}
	print opinionStatDict
	for node in nodeList:
		opinions = D.getAllOpinionById(node)
		opinionCount = len(opinions)
		if(opinionCount in opinionStatDict):
			opinionStatDict[opinionCount] = opinionStatDict[opinionCount] + 1
		else:
			opinionStatDict[opinionCount] = 1

	opinionStat = opinionStatDict.items()

	opinionStat.sort(key = lambda (x,y):x,reverse = False)
	print opinionStat

	nodeCount = reduce(lambda x,y:(0, x[1] + y[1]),opinionStat)[1]


	print nodeCount
	if(nodeCount != len(nodeList)):
		print "WARNING : ",len(nodeList) - nodeCount,"nodes with no opinion at all"
	# print zip(*opinionStat)
	# plt.plot(*zip(*opinionStat))
	# plt.show()

	analyzeTimeData(D)
	
def plotScatter(D,minGoodTime):
	nodeList = D.getNodeList()
	allPost = []
	for node in nodeList:
		allPost = allPost + map(lambda (time,opinion):(time,node), D.getAllOpinionById(node))

	# plt.scatter(*zip(*allPost))
	# plt.plot([minGoodTime, minGoodTime], [0, 600], 'k-', lw=4,color='r' )
	# plt.show()


	alreadyObserved = set()

	allPost.sort(key = lambda (time,node):time)

	visitedPlot = []

	for (time,nodeIndex) in allPost:
		if (not(nodeIndex in alreadyObserved)):
			alreadyObserved.add(nodeIndex)
		visitedPlot = visitedPlot + [(time,len(alreadyObserved))]

	plt.plot(*zip(*visitedPlot))
	plt.plot([minGoodTime, minGoodTime], [0, 600], 'k-', lw=4,color='r' )
	plt.gca().xaxis.grid(True)
	plt.gca().yaxis.grid(True)
	plt.show()

def analyzeTimeData(D):
	opinionFile = file(D.opinionFile)
	lines = opinionFile.readlines()

	timeStampDict = {}

	# postList = []

	for line in lines:
		post = string.split(line)
		# if we have 4 items need to ignore the 3rd item
		modifiedPost = []
		if (len(post) == 4):
			modifiedPost = [post[0],post[2],post[3]]
		else:
			modifiedPost = post
		################################################

		nodeID = int(modifiedPost[0])
		timeStamp = int(modifiedPost[1])
		postSentiment = float(modifiedPost[2])

		if (timeStamp in timeStampDict):
			timeStampDict[timeStamp] = timeStampDict[timeStamp] + 1
		else:
			timeStampDict[timeStamp] = 1

	# print timeStampDict
	print 'total posts :',len(lines)
	print 'total timestamps',len(timeStampDict)

	opinionDict = D.getOpinionDict()
	# print [D.getAllOpinionById(x)[0] for x in D.getNodeList()]
	nodeList = D.getNodeList();
	minGoodTime = max([D.getAllOpinionById(x)[0] for x in nodeList],key = lambda (x,y): x)[0] + 1
	print "minGoodTime = ",minGoodTime

	for x in nodeList:
		if (D.getDiscreteOpinionBeforeTimeById(minGoodTime,x) == None):
			print "ERROR"
			quit()

	print "minGoodTime is Good"

	# TrainCounts = Counter(map(len,[D.getAllOpinionBeforeTimeById(minGoodTime,x) for x in nodeList]))
	# print TrainCounts.items()

	# TestCounts = Counter(map(len,[D.getAllOpinionOnOrAfterTimeById(minGoodTime,x) for x in nodeList]))
	# print TestCounts.items()

	Statistics = [(x,len(D.getAllOpinionBeforeTimeById(minGoodTime,x)),len(D.getAllOpinionOnOrAfterTimeById(minGoodTime,x)),len(D.getInfluencesById(x))) for x in nodeList ]

	goodStatistics = filter(lambda (x,train,test,influences): train > 3 and test > 2 and influences > 0,Statistics)

	# goodStatistics.sort(key = lambda (x,train,test,influences):abs(test - train),reverse = True)
	goodStatistics.sort(key = lambda (x,train,test,influences):test + train + influences,reverse = True)
	print goodStatistics

	print 'total verygood nodes : ',len(goodStatistics)
	
	# print D.getInfluencesById(10452)
	# for (x,y) in TestCounts.items():
	# 	print x
	return minGoodTime

def findAllLonelyNodes(D):
	nodeList = D.getNodeList()
	influenceStat = [(x,len(D.getInfluencesById(x))) for x in nodeList]

	lonelyNodes = filter(lambda (node,influenceCount): influenceCount < 1,influenceStat)
	print lonelyNodes
	print 'total lonely nodes :',len(lonelyNodes)

