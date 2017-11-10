import arcpy
home=arcpy.env.workspace = "C:/Users/mpleasan/Desktop/class8s/working/class8.gdb"
path1 = "C:/Users/mpleasan/Desktop/class8s/"

fcs = arcpy.ListFeatureClasses()
print fcs

sc = arcpy.da.SearchCursor("pointsSP", ['Shape@'])

##for r in sc:
##    print type(r[0]) # ex. output: <class 'arcpy.arcobjects.geometries.PointGeometry'>
##    print r[0].isMultipart # ex. output: False
##    for q in r[0]:  # Accessing the geometry object!!
##        print type(q) # ex. output: <type 'geoprocessing point object'>
##        print q.X, q.Y # ex . output: 575934.185446 614162.241113
##del sc
##
##sc = arcpy.da.SearchCursor("pointsMP", ['Shape@'])
##
##for r in sc:
##    print type(r[0]) 
##    print r[0].isMultipart 
##    for q in r[0]:
###        print type(q) 
##        print q.X, q.Y
##del sc

##sc = arcpy.da.SearchCursor("pointsMP", ['Shape@XY'])
##for r in sc:
##    print type(r[0])
##    print r[0][0], r[0][1]
##
##sc = arcpy.da.SearchCursor("trailsSP", ['Shape@'])
##
### NOW THAT YOU'RE USING LINES, YOU HAVE TO ACCESS THE ARRAY
##
##for r in sc: 
##    print type(r[0]) 
##    print r[0].isMultipart 
##    for q in r[0]:
##        print type(q)
##        for s in q: # THIS IS WHERE YOU ACCESS THE ARRAY, Q IS THE ARRAY
####            print type(s)
##            print s.X, s.Y
##del sc


##sc = arcpy.da.SearchCursor("trailsMP", ['Shape@'])
##
##coords = []
##
##for r in sc: 
##    print type(r[0]) # geometry object
##    print r[0].isMultipart 
##    for q in r[0]: # accessing the arrays that are within the geometry object
##        print type(q) # an array
##        for s in q:
####            print type(s)
####            print s.X, s.Y
##            t = (s.X, s.Y) # Stores tuple of points
##            coords.append(t) # Creating a list of tuples containing the x, y coordinates
##
##del sc
##print coords

##############################################

##f1 = open(path1 + "newStations.txt", "r") # Stores a "file" object in the f1 variable in read mode. This object has methods and properties
##
##ic = arcpy.InsertCursor("pointsSP", ["Shape@"])
##
##for dc in f1.readlines(): # iterates through each line in the file
##    out = dc.split(",") # splits each line by commas, creating lists
##    pt = arcpy.Point(float(out[1]), float(out[2])) # Have to turn the coordinates into floats, because they're decimals
##    ic.insertRow([arcpy.PointGeometry(pt)]) # Creates a PointGeometry, and inserts it
##del ic
##f1.close() # Closes the file

del ic
ic = arcpy.InsertCursor("pointsMP", ["Shape@"])
f1 = open(path1 + "newStations.txt", "r") 
d = {} # Empty dictionary

for dc in f1.readlines():
    out = dc.split(",")
    out[3] = out[3][0] # Accounts for new line characters (line breaks) at the end of the lines in the file
    if out[3] not in d:      
        d[out[3]] = arcpy.Array() # Runs twice, creates arrays for "A" and "B" and stores them in dictionary above ## CREATING ARRAY, WHICH HAS "ADD METHOD"       
    pt = arcpy.Point(float(out[1]), float(out[2]))
    print pt.X, pt.Y
    d[out[3]].add(pt) # Use the add fuction to add the point to the array
f1.close()
for x in d.keys(): #iterates through a list of keys -- not the values
    ic.insertRow([arcpy.Multipoint(d[x])]) # REMEMBER THE BRACKETS HERE

del ic