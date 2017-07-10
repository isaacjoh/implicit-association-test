import numpy as np
import os

#mapped conversion function, changes string block names to integers for numpy array
def block2num(blockString):
	return int(blockString[5:])

#create file for output and write header
outputFile = open("SummaryScores.out", "r+")
if outputFile.read(1) != "I":
	outputFile.write("Identifier        FileName            D-IAT1\n")

#main loop of program goes over all files in directory
for fn in os.listdir('.'):
	filename = fn
	identifier = filename[:filename.find('_')]

	#only parse txt output files
	if os.path.isfile(fn) and fn[-4:] == ".txt":
		rtArray = np.loadtxt(open(fn,"rb"),delimiter=",",usecols=(1,6,10), converters = {1:block2num}  )
		firstIat = rtArray[ rtArray[:,0] <= 7 ,:]
		secondIat = rtArray[ rtArray[:,0] > 7 ,:]

		#throw out subjects where more than 10% of trials are less than 100ms
		if ( sum(firstIat[:,2] < 100) / len(firstIat[:,1]) ) > 0.1 :
			print fn + "   " + "over 10% < 100ms\n"
			continue

		#mean reaction times for relevant blocks
		avg3 = np.mean(rtArray[(firstIat[:,0] == 3), 2])
		avg4 = np.mean(rtArray[(firstIat[:,0] == 4), 2])
		avg6 = np.mean(rtArray[(firstIat[:,0] == 6), 2])
		avg7 = np.mean(rtArray[(firstIat[:,0] == 7), 2])

		#standard deviation over relevant blocks
		std36 = np.std(rtArray[(firstIat[:,0] == 3) | (firstIat[:,0] == 6), 2])
		std47 = np.std(rtArray[(firstIat[:,0] == 4) | (firstIat[:,0] == 7), 2])

		print firstIat[(firstIat[:,0] == 1), 1]

		#Account for the initial randomization of category pairings when calculating
		#the d-score, (0 value == default pairing, value > 1 == switched pairing)
		if sum(firstIat[(firstIat[:,0] == 1), 1]) < 1:
			d1 = (avg6 - avg3) / std36
			d2 = (avg7 - avg4) / std47
		if sum(firstIat[(firstIat[:,0] == 1), 1]) > 1:
			d1 = (avg3 - avg6) / std36
			d2 = (avg4 - avg7) / std47

		dscore1 = (d1 + d2)/2

		print dscore1

		outputFile.write(identifier + '   ' + fn + '   ' + str(dscore1)+ '\n')