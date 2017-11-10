# trees.py
# Purpose: Collect two fields in a dictionary.
# For each unique value in the first field (e.g., species),
#   record in a dictionary only the first occurrence of that
#   value encountered by the cursor (e.g., record only the first 'LOB').
# Usage: input_file
# Example input: C:/gispy/data/ch18/rdu_forest1.dbf SPECIES DBH
import arcpy, sys

fc = sys.argv[1]
field1 = sys.argv[2]
field2 = sys.argv[3]
tDict = {}

# Populate dictionary with species:field1:field2.
sc = arcpy.da.SearchCursor(fc, [field1, field2])
for row in sc:
    k = row[0]
    val = row[1]
    if k not in tDict:
        tDict[k] = val
del sc

print 'Dictionary of firsts: \n{0}'.format(tDict)
