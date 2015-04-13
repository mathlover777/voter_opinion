def removePostId(inputFile,outputFile):
	# removes the postids from the reddit data set use it only once
	with open(inputFile,"r") as fp:
		with open(outputFile,"w") as wp:
			postList = fp.readlines()
			modifiedPostList = map(lambda x:x[0]+" "+x[2]+" "+x[3]+"\n",map(lambda x:x.split(),postList))
			wp.writelines(modifiedPostList)


inputFile = 'Reddit/post_with_postid.txt'
outputFile = 'Reddit/post.txt'

removePostId(inputFile,outputFile)
