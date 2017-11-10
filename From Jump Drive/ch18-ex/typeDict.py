# typeDict.py
# Purpose: Use a dictionary to collect the names and types of file
# Usage: input_directory
# Example input: C:/gispy/data/ch18/smallDir
import os, sys, arcpy
inputDir = sys.argv[1]
fileList = os.listdir(inputDir)
arcpy.env.workspace = inputDir
tDict = {}
for f in fileList:
    desc = arcpy.Describe(f)
    fType = desc.DataType
    if fType not in tDict:
        tDict[fType] = [f]  # Add a new item to the dictionary.
    else:
        tDict[fType].append(f)  # Update an item by adding to an item's list.

print 'Type dictionary: \n{0}'.format(tDict)
