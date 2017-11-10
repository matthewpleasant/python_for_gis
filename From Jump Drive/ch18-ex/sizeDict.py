# sizeDict.py
# Purpose: Use a dictionary to collect the names and sizes of file
#          in an input directory, than find the average size
# Usage: input_directory
# Example input: C:/gispy/data/ch18/smallDir
import os, sys
inputDir = sys.argv[1]
fileList = os.listdir(inputDir)

sDict = {}
for f in fileList:
    size = os.path.getsize(inputDir + '/' + f)
    sDict[f] = size

print 'Size dictionary: \n{0} \n'.format(sDict)
sizes = sDict.values()
total = sum(sizes)
count = len(sizes)
avg = float(total)/count
print 'Avergage file size: {0}'.format(avg)
