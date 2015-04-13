################ used in actual experiment ################
datasetName = 'Reddit'
# datasetName = 'Twitter'
# datasetName = 'Synthetic'

trainPercentage = .9 # timestamp setting is not needed any more , just set this and timestamp 
# will be automatically set

# timestamp = 1355750721 #reddit uncleaned
timestamp = 60909 # cleaned separator for Reddit DataSet
# timestamp = 87 # cleaned separator for Twitter Dataset
########## separator means that train before this timestamp and test 
# after this time stamp
######### need to automate this adjustment in the config file
########## depending on the the 'datasetName'

# timestamp = 40 # used in synthetic also


maxTime = 64186 # last observed timestamp for cleaned Reddit Data
# how ever max time used only in create_synthetic for synthetic data creation
# and in evaluate which is used for synthetic evaluation
# for actual data sets we use the evaluate_actual and we dont need
# maxTime in it
# maxTime = 50 # used in synthetic also
######## the learned adjaceny
adjacencyName = datasetName + '_' + str(timestamp) + '_adjacency.json'


resultFile_pernode_using_lastOriginal = datasetName + '/Result_pernode_using_lastOriginal.json'
resultFile_pernode_using_lastPredicted = datasetName + '/ResultFile_pernode_using_lastPredicted.json'
############################
##################################################


# used to create the clean data set
nodeListFile = '/nodeList.txt'
edgeListFile = '/edgeList.txt'
postFile = '/post.txt'
###################################

# these are used in train
nodeListFile_clean = '/nodeList_clean.txt'
edgeListFile_clean = '/edgeList_clean.txt'
postFile_clean = '/post_clean.txt'
#########################


########### used for synthetic dataset creator #################
synthetic_nodeList = 'Synthetic/nodeList_clean.txt'
synthetic_edgeList = 'Synthetic/edgeList_clean.txt'
synthetic_postFile = 'Synthetic/post_clean.txt'

synthetic_positive_opinion = 1 # the opposite one will be negative of this

nodeIdToIndexMap = '/nodeIdToIndexMap.txt' # these are not required for train.py
nodeIndexToIdMap = '/nodeIndexToIdMap.txt' # only required for recovering , module not implemented yet
timeStampToTimeIndexFile = '/timeStampToTimeIndexFile.txt'
timeIndexToTimeStampFile = '/timeIndexToTimeStampFile.txt'


synthetic_weights = 'Synthetic/random_weights.json'
synthetic_adjacency = 'Synthetic/adjacency.json'
synthetic_opinions = 'Synthetic/opinions.json'
num_nodes = 200
edge_prob = .5
#################################################################

############## used to log mosek failures #######################
failureLog = 'failure.txt'
################################################################


# method that must be run to update some config values automatically
def init_config():
	D = datahandler.Datahandler(config.datasetName)
	maxTime = D.getTimeStampCount()
	timestamp = int(maxTime * trainPercentage)
