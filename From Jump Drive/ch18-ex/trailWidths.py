# trailWidths.py
# Purpose: Use a dictionary to calculate trail statistics.
# Usage: fullpath_filename classification_fieldname trail_width_fieldname
# Example input: C:/gispy/data/ch18/narniaHike.shp Classifica Tra_Width
# Example input 2: C:/gispy/data/ch18/2010_SENT_Single_T.shp Classifica Trail_Widt
import arcpy, sys

fc = sys.argv[1]
field1 = sys.argv[2]
field2 = sys.argv[3]
tDict = {}


# Populate dictionary with species:field1:field2.
sc = arcpy.da.SearchCursor(fc, [field1, field2])
for row in sc:
    k = row[0]
    val = float(row[1])
    if k in tDict:
        tDict[k].append(val)
    else:
        tDict[k] = [val]
del sc

print '{0}_{1}_Dict = {2}'.format(field1, field2, tDict)
for k, v in tDict.items():
    avg = sum(v)/len(v)
    print '{0}: {1}, average {2}: {3:.2f}'.format(field1, k, field2, avg)

##values = tDict.values()
##minVal = min(values)
##maxVal = max(values)
##
##print 'Minimum  {0} = {1}'.format(field2,minVal)
##
##print 'Features(s) with minimum {0}:'.format(field2),
##vals = findVal(tDict, minVal)
##for v in vals:
##    print v,
##
##print '\nMaximum {0} = {1}'.format(field2, maxVal)
##print 'Features(s) with maximum {0}:'.format(field2),
##vals = findVal(tDict, maxVal)
##for v in vals:
##    print v,
