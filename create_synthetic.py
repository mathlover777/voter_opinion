import networkx as NX
import config
import utility
import copy
import random

def create_Graph(num_nodes, edge_prob):
	# G = NX.erdos_renyi_graph(num_nodes, edge_prob, None, True)
	# G = NX.complete_graph(num_nodes)
	G = NX.fast_gnp_random_graph(num_nodes, edge_prob, None, False)
	graph = []	

	for i in xrange(0,num_nodes):
		temp_graph = []
		graph.append(temp_graph)

	for (i,j) in G.edges():
		graph[i].append(j)

	# print graph
	# print G.edges()

	return graph


def create_matrix(G):

	mat = []

	for i in xrange(0,len(G)):
		temp_graph = [0]*len(G)
		mat.append(temp_graph)

	for i in xrange(0,len(G)):
		for j in xrange(0, len(G[i])):
			mat[i][G[i][j]] = 1

	# print mat
	return mat

def create_initial_opinions(OpinionVal, num_nodes):

	# from random import randint

	opinions = []

	for i in xrange(0,num_nodes):
		tempVal = random.randint(0,1)

		if tempVal == 1:
			opinions.append(OpinionVal)
		else:
			opinions.append(-OpinionVal)
	
	# print opinions
	return opinions

def transition_prob(G, LastOpinion, currnode,X = None):

	P = 0.0
	if(X == None):
		K = len(G[currnode])
		for i in xrange(0, K):
			temp_node = G[currnode][i]
			if LastOpinion[currnode] != LastOpinion[temp_node]:
				P += (1.0/float(K))
	else:
		for influence in G[currnode]:
			if LastOpinion[currnode] != LastOpinion[influence]:
				P = P + X[currnode][influence]
	return P

def computeAllTransitionProbability(G,previousOpinionVector,X = None):
	A = range(0,len(G))
	transitonProbabilities = map(lambda x: transition_prob(G,previousOpinionVector,x,X),A)
	return transitonProbabilities

def update_opinions(G, num_nodes, maxTime, OpinionValue,X = None):
	Opinions = []
	Opinions.append(create_initial_opinions(OpinionValue, num_nodes))

	for time in xrange(0,maxTime):
		transitonProbabilities = computeAllTransitionProbability(G,Opinions[time],X)
		maxProbability = max(transitonProbabilities)
		print 'maxprob = ',maxProbability
		# transProb = 0
		new_opinion = [0] * num_nodes
		for currnode in xrange(0,num_nodes):
			transProb = transition_prob(G, Opinions[time],currnode,X)
			# if(transitonProbabilities[currnode] == maxProbability):
			# 	transProb = 1.0
			# else:
			# 	transProb = 0.0
			# print transProb, currnode, time
			if transProb >= 0.5:
				new_opinion[currnode] = -1 * Opinions[time][currnode]
				print 'transitoning node - ',currnode,' at time ',time,' from ',Opinions[time][currnode],' to ',new_opinion[currnode]
			else:
				new_opinion[currnode] = Opinions[time][currnode]
		Opinions.append(new_opinion)

	# print Opinions
	return Opinions

def fileHandling(G, num_nodes, Opinions, maxTime):
	nodeFile = open(config.synthetic_nodeList,'w+')
	edgeFile = open(config.synthetic_edgeList,'w+')
	opinionFile = open(config.synthetic_postFile,'w+')

	MG = create_matrix(G)
	for i in xrange(0,num_nodes):
		nodeFile.write(str(i)+"\n")
		for j in xrange(0, num_nodes):
			if MG[j][i] == 1:
				edgeFile.write(str(i) + " " + str(j) + "\n")

		for time in xrange(0, maxTime):
			opinionFile.write(str(i) + " " + str(time) + " " + str(Opinions[time][i]) + "\n")

	nodeFile.close()
	edgeFile.close()
	opinionFile.close()

def createRandomWeightMatrix_voter(M):
	nodeCount = len(M)
	X = []
	for node in xrange(0,nodeCount):
		X = X + [{}]
		weights = [1.0] * len(filter(lambda x:x == 1,M[node]))
		# print filter(lambda x:x == 1,M[node])
		# weights = map(lambda x: random.uniform(0.0,1.0),weights)
		# weights = map(lambda x: random.uniform(0.0,1.0),weights)
		sumWeights = sum(weights)
		weights = map(lambda x: x / sumWeights,weights )
		j = 0
		for i in xrange(0,nodeCount):
			if(M[node][i] == 1):
				X[node][i] = weights[j]
				j = j + 1
			# else:
			# 	X[node][i] = 0.0
	return X



def saveOpinions(Opinions):

	saveOpinionsDict = {}
	time = 0
	for opinionAtT in Opinions:
		opinionAtTDict = {}
		index=0
		for opinionVals in opinionAtT:
			opinionAtTDict[index] = opinionVals
			index = index+1
		saveOpinionsDict[time] = opinionAtTDict
		time = time+1

	# print saveOpinionsDict

	utility.saveAsJson(saveOpinionsDict, config.synthetic_opinions)


def voterModel(num_nodes, edge_prob, maxTime):

	OpinionValue = config.synthetic_positive_opinion
	G = create_Graph(num_nodes,edge_prob)
	X = createRandomWeightMatrix_voter(create_matrix(G))

	Opinions = update_opinions(G, num_nodes, maxTime, OpinionValue,X)

	fileHandling(G, num_nodes, Opinions, maxTime)

	saveOpinions(Opinions)
	
	utility.saveAsJson(X,config.synthetic_weights)
	utility.saveAsJson(G,config.synthetic_adjacency)

if __name__ == '__main__':

	# num_nodes = 
	# edge_prob = 0.009
	# maxTime = 50

	voterModel(config.num_nodes, config.edge_prob, config.maxTime)