from __future__ import with_statement

import sys
from mosek import iparam
import mosek
import numpy as np

inf = 0.0

def streamprinter(text):
    # sys.stdout.write(text)
    # sys.stdout.flush()
    return

def solveConcave(constraints,expressionList):
	solution = []

	# print 'constraint'
	# print constraints

	# print '\n'.join([ str(myelement) for myelement in expressionList ])
	# print len(expressionList)


	sub = fill_sub(constraints, expressionList)
	asub = fill_asub(constraints, expressionList)
	acof  = fill_aval(constraints, expressionList,asub)
	ptrb = fill_ptrb(asub)
	ptre = fill_ptre(asub)
	actualNumVar = len(constraints)
	numvar = len(expressionList)+len(constraints)
	numcon = len(expressionList)+1


	# bkx   = fill_bkx(len(constraints), len(expressionList))
	# blx   = fill_blx(len(constraints), len(expressionList))
	# bux   = fill_bux(len(constraints), len(expressionList))

	bkx   = fill_bkx(len(constraints), len(expressionList))
	blx   = fill_blx(len(constraints), len(expressionList))
	bux   = fill_bux(len(constraints), len(expressionList))

	asub = convertListToArray(asub)
	# print 'bkx',bkx
	# print 'blx',blx
	# print 'bux',bux
	# print "asub : ", asub

	with mosek.Env() as env:
		env.set_Stream (mosek.streamtype.log, streamprinter)
		with env.Task(0,0) as task:
			task.set_Stream (mosek.streamtype.log, streamprinter)	

			bkc = [mosek.boundkey.ra]
			for i in xrange(0,len(expressionList)):
				bkc.append(mosek.boundkey.fx)
			blc = [0.0]
			for expression in expressionList:
				blc.append(-expression[1])

			buc = [1.0]
			for expression in expressionList:
				buc.append(-expression[1])
			# print 'bkc',bkc
			# print 'blc',blc
			# print 'buc',buc

			aval  = acof		      

			task.appendvars(numvar)
			task.appendcons(numcon)

			task.putobjsense(mosek.objsense.minimize)

			task.putvarboundslice(0, numvar, bkx, blx, bux)
			task.putconboundslice(0, numcon, bkc, blc, buc)

			task.putacollist(sub, ptrb, ptre, asub, aval ) # as we are using row format


			opro  = []
			for i in xrange(0,len(expressionList)):
				opro.append(mosek.scopr.log)
			# print "opro ",opro

			oprjo = []
			for i in xrange(0,len(expressionList)):
				oprjo.append(len(constraints)+i)
			# print "oprjo ",oprjo


			oprfo = []
			oprgo = []
			oprho = []
			oprho = map(lambda (x,y):0.0,expressionList)

			for i in xrange(0,len(expressionList)):
				oprfo.append(-1.0)
				oprgo.append(1.0)

			# print "oprfo ", oprfo
			# print "oprgo", oprgo
			# print "oprho",oprho

			oprc  = []
			opric = []
			oprjc = []
			oprfc = []
			oprgc = []
			oprhc = []
			
			task.putSCeval(opro, oprjo, oprfo, oprgo, oprho,
				oprc, opric, oprjc, oprfc, oprgc, oprhc)
			
			task.optimize()

			res = [ 0.0 ] * numvar
			task.getsolutionslice(mosek.soltype.itr,mosek.solitem.xx,0, numvar,res)
			res = res[0:actualNumVar]
			# print ( "Solution : %s" % res )
			solution = res
			# print 'SUM : ',sum(solution)

	return solution


def fill_sub(constraints,expressionList):
	sub = []
	for i in xrange(0,len(constraints)+len(expressionList)):
		sub.append(i)
	# print "sub ",sub
	return sub


def fill_asub(constraints, expressionList):
	asub = []

	for i in xrange(0,len(constraints)):
		asub.append(set([0]))

	for i in xrange(0,len(expressionList)):
		asub.append(set([i+1]))

	for i in xrange(0,len(expressionList)):
		variableIndexList = getVariableIndexes(i,expressionList)
		for varIndex in variableIndexList:
			asub[varIndex].add(i+1)

	for i in xrange(0,len(asub)):
		asub[i] = list(asub[i])

	# print asub
	return asub

def fill_aval(constraints, expressionList, asub):
	# need to review this  code
	aval = []

	for i in xrange(0,len(constraints)):
		aval.append([1.0])

	for i in xrange(0,len(expressionList)):
		aval.append([-1.0])

	for i in xrange(0,len(constraints)):
		for index in asub[i]:
			if index==0:
				continue
			aval[i].append(giveCoefficient(i,expressionList,index-1))

	aval = convertListToArray(aval)
	# print "aval ",aval
	return aval


def convertListToArray(temp_list):
	ret = reduce(lambda x,y:x+y,temp_list)
	return ret

def fill_ptrb(asub):
	ret = [0]
	index = 0
	for x in asub[:-1]:
		ret.append(index + len(x))
		index = index + len(x)
	# print "ptrb ",ret
	return ret

def fill_ptre(asub):
	ret = []
	index = 0
	for x in asub:
		ret.append(index + len(x))
		index = index + len(x)
	# print "ptre ", ret
	return ret

def fill_bkx(constraintsSize, expressionListSize):
	bkx = []

	for x in xrange(0,constraintsSize):
		bkx.append(mosek.boundkey.ra)

	for x in xrange(0,expressionListSize):
		# bkx.append(mosek.boundkey.ra)
		bkx.append(mosek.boundkey.lo)

	# print bkx
	return bkx

def fill_blx(constraintsSize, expressionListSize):
	blx = []

	for x in xrange(0,constraintsSize):
		blx.append(0.0)

	for x in xrange(0,expressionListSize):
		blx.append(0.0)

	# print blx
	return blx

def fill_bux(constraintsSize, expressionListSize):
	bux = []

	for x in xrange(0,constraintsSize):
		bux.append(1.0)

	for x in xrange(0,expressionListSize):
		# bux.append(1.0)
		bux.append(np.inf)

	# print bux
	return bux

def getVariableIndexes(expressionIndex,expressionList):
	retList = []
	(x,y) = expressionList[expressionIndex]
	for (i,j) in x:
		retList.append(i)
	# print retList
	return retList

def giveCoefficient(variableIndex,expressionList,expressionIndex):
	# returns co-efficient if not 0
	# else None
	(x,y) = expressionList[expressionIndex]
	for (i,j) in x:
		if variableIndex==i:
			return j
	return None
# *****************************************************