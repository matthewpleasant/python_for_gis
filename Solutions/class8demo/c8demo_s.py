import arcpy
home=arcpy.env.workspace = "D:/Dropbox/pgis_fall2017/class8i/working/class8.gdb"
path1 = "D:/Dropbox/pgis_fall2017/class8i/"

# coords = []
sc = arcpy.da.SearchCursor("pointsSP",["Shape@"])
for r in sc:
    print type(r[0])
    print r[0].isMultipart
    for q in r[0]:
        print type(q)
        print q.X, q.Y
#        tuple1 = t.x, t.y
#        coords.append(tuple1)
#print coords

sc = arcpy.da.SearchCursor("pointsMP",["Shape@"])
for r in sc:
    print type(r[0])
    print r[0].isMultipart
    for t in r[0]:
        print type(t)
        print t.X, t.Y

sc = arcpy.da.SearchCursor("pointsSP",["Shape@XY"])
for r in sc:
    print type(r[0])
    print r[0][0], r[0][1]

sc = arcpy.da.SearchCursor("pointsMP",["Shape@XY"])
for r in sc:
    print type(r[0])
    print r[0][0], r[0][1]

sc = arcpy.da.SearchCursor("trailsSP",["Shape@"])
for r in sc:
    # print r[0].isMultipart
    for q in r[0]:
        print type(q)
        for s in q:
            print s.X, s.Y
    print "end of feature"

sc = arcpy.da.SearchCursor("trailsMP",["Shape@"])
for r in sc:
    # print r[0].isMultipart
    for q in r[0]:
        print type(q)
        for s in q:
            print s.X, s.Y
    print "end of Feature"




ic = arcpy.da.InsertCursor("pointsSP","Shape@")
f1 = open(path1+"NewStations.txt","r")
for line in f1.readlines():
    out=line.split(",")
    pt = arcpy.Point(float(out[1]),float(out[2]))
    ic.insertRow([arcpy.PointGeometry(pt)])
del ic
f1.close()

ic = arcpy.da.InsertCursor("pointsMP","Shape@")
f1 = open(path1+"NewStations.txt","r")
d = {} # creates an empty dictionary - no items (key/value pairs) 
for line in f1.readlines(): # reads in all lines simultaneously but then loops thru each line in order
    out=line.split(",") # splits the string based on where the commas are 
    out[3] = out[3][0] #This has the effect of taking just the first character in the string
                                  # so as to strip away the possibility of hidden linefeed characters 
    if out[3] not in d: # this tests whether the value of out[3] is currently a key in the dictionary
                                  # in this example this will happen once for 'A' and once for 'B'
        d[out[3]] = arcpy.Array() # if the value of out[3] is not a current key, the key in the
                                                  # dictionary is created and it references a value which is
                                                  # initially set to an empty Array object
    d[out[3]].add(arcpy.Point(float(out[1]),float(out[2]))) # this takes the values of out[1] and
                                                                                             # out[2], changes them to floats, creates a
                                                                                             # Point object from them and then adds the point to the
                                                                                             # array that is referenced by the out[3] key in the dictionary
# after the above loop, we have a dictionary with 2 items - i.e. 2 key/value pairs
# the keys are 'A' and 'B' and their values are arrays that contain all the points associated with A/B in the input file
f1.close()
for x in d.keys():    # this loops thru the dictionary keys, so x takes values of 'A' and 'B'
    ic.insertRow([arcpy.Multipoint(d[x])]) # a multipoint geometry is created from the array referenced by the dictionary key
                                                                    # and then this geometry is inserted into the feature class bu the insertRow method of
                                                                    # the insert cursor
del ic

