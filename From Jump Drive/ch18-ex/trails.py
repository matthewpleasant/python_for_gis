# trails.py
# Purpose: Use a dictionary to calculate trail statistics.
# Usage: fullpath_filename unique_id_fieldname trail_width_fieldname
# Example input1: C:/gispy/data/ch18/narniaHike.shp FID Tra_Width
# Example input2: C:/gispy/data/ch24/USstates/USA_States_Generalized.shp STATE_NAME MED_AGE

import arcpy, sys

fc = sys.argv[1]
field1 = sys.argv[2]
field2 = sys.argv[3]
tDict = {}


def findVal(dict, val):
    '''Return a list of keys that are mapped to val.'''
    keys = []
    for k, v in dict.items():
        if v == val:
            keys.append(k)
    return keys

# Populate dictionary with species:field1:field2.
sc = arcpy.da.SearchCursor(fc, [field1, field2])
for row in sc:
    k = row[0]
    val = float(row[1])
    tDict[k] = val
del sc

print '{0}_{1}_Dict = {2}'.format(field1, field2, tDict)

values = tDict.values()
minVal = min(values)
maxVal = max(values)

print 'Minimum  {0} = {1}'.format(field2, minVal)

print 'Features(s) with minimum {0}:'.format(field2),
vals = findVal(tDict, minVal)
for v in vals:
    print v,

print '\nMaximum {0} = {1}'.format(field2, maxVal)
print 'Features(s) with maximum {0}:'.format(field2),
vals = findVal(tDict, maxVal)
for v in vals:
    print v,
