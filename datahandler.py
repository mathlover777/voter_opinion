import string
import random
import utility
import config

class Datahandler:

# ################## init function ################################
	def __init__(self,datasetName):
		self.datasetName = datasetName
		self.__initNodeList(datasetName)
		self.__initAdjacencyList(datasetName)
		self.__initOpinionList(datasetName)


	def __initNodeList(self,datasetName):
		self.nodeFile = self.datasetName + config.nodeListFile_clean
		nodeFile = open(self.nodeFile)
		lines = nodeFile.readlines()
		self.nodeList = []
		i = 0
		for line in lines:
			self.nodeList = self.nodeList + [int(line)]

	def __initOpinionList(self,datasetName):
		self.opinionFile = self.datasetName + config.postFile_clean
		opinionFile = file(self.opinionFile)
		lines = opinionFile.readlines()
		self.opinionDict = []
		for node in self.nodeList:
			self.opinionDict = self.opinionDict + [[]]

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

			if(postSentiment == 0.0 or postSentiment == None):
				postSentiment = -1.0

			self.opinionDict[nodeID] = self.opinionDict[nodeID] + [(timeStamp,postSentiment)]
		for node in self.nodeList:
			self.opinionDict[node].sort(key=lambda (x,y): x, reverse = False)

	def __initAdjacencyList(self,datasetName):
		self.edgeList = self.datasetName + config.edgeListFile_clean
		self.edgeDict = []
		for node in self.nodeList:
			self.edgeDict = self.edgeDict + [[]]
		edgeFile = file(self.edgeList)
		lines = edgeFile.readlines()
		for line in lines:
			(a,b) = string.split(line) # a influences b (directed)
			a = int(a)
			b = int(b)
			self.edgeDict[b] = self.edgeDict[b] + [a]

	def saveAsJson(self):
		utility.saveAsJson(self.nodeList,'nodeListTemp.json')
		utility.saveAsJson(self.opinionDict,'opinionDictTemp.json')
		utility.saveAsJson(self.edgeDict,'edgeDictTemp.json')

##################################################################


######################## functions accessed by nodeID ###############################
	def getInfluencesById(self,nodeId): # gets the list of influences
		return self.edgeDict[nodeId]

	def getDiscreteInfluenceOpinionsById(self,timestamp,nodeId): # get latest opinion of influences DISCRETE
		return map(lambda x:(x,self.getDiscreteOpinionBeforeTimeById(timestamp,x)),self.edgeDict[nodeId])

	def getAllOpinionById(self,nodeId): # get all opinions for a node
		return self.opinionDict[nodeId]

	def getAllOpinionBeforeTimeById(self,timestamp,nodeId): # get all opinions < time for a node
		return filter(lambda (time,opinion): time < timestamp, self.opinionDict[nodeId])

	def getAllOpinionOnOrAfterTimeById(self,timestamp,nodeId): # get all opinions >= time for a node
		return filter(lambda (time,opinion): time >= timestamp,self.opinionDict[nodeId])

	def getAllDiscreteOpinionBeforeTimeById(self,timestamp,nodeId): # get all opinions < time for a node DISCRETE
		return map(lambda (time,opinion):(time,0 if opinion < 0.0 else 1),self.getAllOpinionBeforeTimeById(timestamp,nodeId))

	def getAllDiscreteOpinionOnorAfterTimeById(self,timestamp,nodeId): # get all opinions >= time for a node DISCRETE
		return map(lambda (time,opinion):(time,0 if opinion < 0.0 else 1),self.getAllOpinionOnOrAfterTimeById(timestamp,nodeId))		

	def getOpinionBeforeTimeById(self,timestamp,nodeId):
		# gives all opinion for a node strictly before a timeStamp
		# nodes are selected by ID
		prevX = -1
		prevY = -1
		found = 0
		for (x,y) in self.opinionDict[nodeId]: # need to replace by binary search
			if x >= timestamp:
				if (found == 0):
					return None
				return (prevX,prevY)
			prevY = y
			prevX = x
			found = found + 1
		return (prevX,prevY)

	def getDiscreteOpinionBeforeTimeById(self,timestamp,nodeId):
		opinion = self.getOpinionBeforeTimeById(timestamp,nodeId)
		# print (timestamp,nodeId,opinion)
		if(opinion == None):
			return None
		opinionValue = opinion[1]
		# if(opinionValue > 0):
		# 	return 1
		# if(opinionValue < 0):
		# 	return 0
		return self.continousToDiscteteOpinion(opinionValue)

	def getTimeStampCount(self):
		# if the time stamps are t0,t1, .... ,tn-1 then this will return n
		return max(map(lambda nodeOpinions: max(map(lambda (time,opinion): time,nodeOpinions)),self.opinionDict)) 

	def continousToDiscteteOpinion(self,opinionValue):
		if(opinionValue > 0):
			return 1
		if(opinionValue < 0):
			return 0

	def getOpinionIfAvailableByNodeId(self,timestamp,nodeId):
	    minTime = 0
	    maxTime = len(self.opinionDict[nodeId])-1
	    while True:
	    	if maxTime < minTime:
	    		return None
	    	midTime = (maxTime + minTime) // 2
	    	if self.opinionDict[nodeId][midTime][0] < timestamp:
	    		minTime = midTime + 1
	    	elif self.opinionDict[nodeId][midTime][0] > timestamp:
	    		maxTime = midTime - 1
	    	else:
	    		return self.continousToDiscteteOpinion(self.opinionDict[nodeId][midTime][1])
	def getOpinionsForAllNodesIfAvailable(self,timestamp):
		opinionList = {}
		for nodeId in self.nodeList:
			currentOpinion = self.getOpinionIfAvailableByNodeId(timestamp,nodeId)
			if(currentOpinion != None):
				opinionList[nodeId] = currentOpinion
			else:
				pass
		return opinionList
######################### functions to access private data #########################
	def getNodeList(self):
		return self.nodeList
	def getOpinionDict(self):
		return self.opinionDict
	def getNodeCount(self):
		return len(self.nodeList)
#################### test functions ###############################################