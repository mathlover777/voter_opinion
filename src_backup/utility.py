import sys
import json
def drawProgressBar(percent,msg, barLen = 100):
    sys.stdout.write("\r")
    progress = ""
    for i in range(barLen):
        if i < int(barLen * percent):
            progress += "="
        else:
            progress += " "
    sys.stdout.write("[ %s ] %.2f%% [%s]" % (progress, percent * 100,msg))
    sys.stdout.flush()
def saveDictionaryAsJson(A,filename):
	with open(filename,'wb') as fp:
	    json.dump(A,fp,indent = 4)

def saveAsJson(A,filename):
    with open(filename,'wb') as fp:
        json.dump(A,fp,indent = 4)