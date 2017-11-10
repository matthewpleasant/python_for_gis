import arcpy, random
path1 = "C:/users/sreader/Dropbox/pgis_fall2017/class9i/c9demo1/"
if arcpy.Exists(path1 + "working/class9a.gdb"):
    arcpy.Delete_management(path1 + "working/class9a.gdb")
arcpy.Copy_management(path1+"class9a.gdb", path1 + "working/class9a.gdb")

home=arcpy.env.workspace = path1+"working/class9a.gdb"

sc = arcpy.da.SearchCursor("pointsSP",["Shape@"])
for r in sc:
    for q in r[0]:
        print type(q)
        print q.X, q.Y

sc = arcpy.da.SearchCursor("pointsMP",["Shape@"])
for r in sc:
    for t in r[0]:
        print type(t)
        print t.X, t.Y

sc = arcpy.da.SearchCursor("trailsSP",["Shape@"])
for r in sc:
    for q in r[0]:
        for s in q:
            print s.X, s.Y
    
sc = arcpy.da.SearchCursor("trailsMP",["Shape@"])
for r in sc:
    for q in r[0]:
        for s in q:
            print s.X, s.Y

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
d = {}
for line in f1.readlines():
    out=line.split(",")
    out[3] = out[3][0]
    if out[3] not in d:
        d[out[3]] = arcpy.Array()
    d[out[3]].add(arcpy.Point(float(out[1]),float(out[2])))
f1.close()
for x in d.keys():    
    ic.insertRow([arcpy.Multipoint(d[x])])
del ic

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

# Below same as MP Point 
ic = arcpy.da.InsertCursor("trailsSP","Shape@")
f1 = open(path1+"NewTrails.txt","r")
d = {}
for line in f1.readlines():
    out=line.split(",")
    if out[1] not in d:
        d[out[1]] = arcpy.Array()
    d[out[1]].add(arcpy.Point(float(out[2]),float(out[3])))
f1.close()
for x in d.keys():    
    ic.insertRow([arcpy.Polyline(d[x])])
del ic

# Below is wrong - would join up separate lines
ic = arcpy.da.InsertCursor("trailsMP","Shape@")
f1 = open(path1+"NewTrails.txt","r")
d = {}
for line in f1.readlines():
    out=line.split(",")
    if out[4] not in d:
        d[out[4]] = arcpy.Array()
    d[out[4]].add(arcpy.Point(float(out[2]),float(out[3])))
f1.close()
for x in d.keys():    
    ic.insertRow([arcpy.Polyline(d[x])])
del ic


#  MP Line/Poly (corrected from class version)
ic = arcpy.da.InsertCursor("trailsMP","Shape@")
f1 = open(path1+"NewTrails.txt","r")
arr = arcpy.Array()
d = {}
LID = -99
for line in f1.readlines():
    out=line.split(",")
    out[4] = out[4].replace("\n","")
    if out[4] not in d:
        d[out[4]] = arcpy.Array()
    if LID == -99:
        LID = out[1]
    if not LID == out[1]:
        d[k].add(arr)
        arr.removeAll()
    arr.add(arcpy.Point(float(out[2]),float(out[3])))
    LID = out[1]
    k = out[4]
f1.close()
d[out[4]].add(arr)
for x in d.keys():    
    ic.insertRow([arcpy.Polyline(d[x])])
del ic

uc = arcpy.da.UpdateCursor("pointsMP","Shape@")
off = [-2000,2000]
arr = arcpy.Array()
for r in uc:
    for p in r[0]:
        pX = p.X + random.choice(off)
        pY = p.Y + random.choice(off)
        pt = arcpy.Point(pX,pY)
        arr.add(pt)
    uc.updateRow([arcpy.Multipoint(arr)])
    arr.removeAll()
del uc

uc = arcpy.da.UpdateCursor("trailsMP","Shape@")
off = [-2000,2000]
arr1 = arcpy.Array()
arr2 = arcpy.Array()
for r in uc:
    for p in r[0]:
        for s in p:
            sX = s.X + random.choice(off)
            sY = s.Y + random.choice(off)
            pt = arcpy.Point(sX,sY)
            arr1.add(pt)
        arr2.add(arr1)
        arr1.removeAll()
    uc.updateRow([arcpy.Polyline(arr2)])
    arr2.removeAll()
del uc

flds = ["Vehicles","Personnel","Category","District"]
uc = arcpy.da.UpdateCursor("sites", flds)
for r in uc:
#    print r[0], r[1], r[2], r[3]
    if r[0] < 10 and r[1] < 20:
        r[2] = "A"
    elif r[0] < 15 and r[1] > 20:
        r[2] = "B"
    else:
        r[2] = "C"
    if r[3] == "Paxton": r[3] = "Reader"
    uc.updateRow(r)
del uc 

flds = ["Vehicles","Personnel","Category","District", "Shape@"]
uc = arcpy.da.UpdateCursor("sites", flds)
for r in uc:
    if r[0] < 10 and r[1] < 20:
        r[2] = "A"
    elif r[0] < 15 and r[1] > 20:
        r[2] = "B"
    else:
        r[2] = "C"
    if r[3] == "Paxton": r[3] = "Reader"
    uc.updateRow(r)
    if r[3] == "Berry":
        uc.deleteRow()
    if r[3] == "Reader":
        for a in r[4]:
            a.X = a.X+5000
            a.Y = a.Y+5000
            pt = arcpy.Point(a.X, a.Y)
            r[4] = arcpy.PointGeometry(pt)
    uc.updateRow(r)    
del uc 

