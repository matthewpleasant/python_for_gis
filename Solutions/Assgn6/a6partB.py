import arcpy, string

arcpy.env.workspace = "C:/users/sreader/Dropbox/pgis_fall2017/class9i/a6partBdemo"
if arcpy.Exists("westeast.shp"):
                arcpy.Delete_management("westeast.shp")
if arcpy.Exists("all.shp"):
                arcpy.Delete_management("all.shp")

arcpy.env.overwriteOutput = 1

arcpy.Intersect_analysis("trails.shp ; floodplain.shp", "outpts.shp","NO_FID","","POINT")

dict1 = {}
dval = 1
flds = ["SHAPE@"]
sc = arcpy.da.SearchCursor("outpts.shp",flds)
for row in sc:
    for b in row[0]:
        ptx = b.X
        pty = b.Y
        key = str(ptx) + " " + str(pty)
        if key not in dict1:
            dict1[key] = dval
del sc        

# W-E
arcpy.CreateFeatureclass_management(arcpy.env.workspace, "westeast.shp", "POLYLINE", "","","","trails.shp")
ic = arcpy.da.InsertCursor("westeast.shp","SHAPE@")
arr = arcpy.Array()
listxy = dict1.keys()
listxy.sort()
for y in listxy:
    v = y.split(" ")
    pt = arcpy.Point(v[0],v[1])
    arr.add(pt)
ic.insertRow([arcpy.Polyline(arr)])
del ic

# ALL 
listxy = dict1.keys()
listyx=[]
for i in listxy:
    j = i.split(" ")
    listyx.append(j[1] + " " + j[0])
arcpy.CreateFeatureclass_management(arcpy.env.workspace, "all.shp", "POLYLINE", "","","","trails.shp")
ic = arcpy.da.InsertCursor("all.shp","SHAPE@")
arr = arcpy.Array()
listxy.sort()
listyx.sort()
we = listxy
sn = listyx
listxy.reverse()
listyx.reverse()
ew = listxy
ns = listyx
all = [we,sn,ew,ns]
# SP
for x in all:
    for y in x:
        v = y.split(" ")
        if x == we or x == ew:
            pt = arcpy.Point(v[0],v[1])
        else:
            pt = arcpy.Point(v[1],v[0])
        arr.add(pt)
    ic.insertRow([arcpy.Polyline(arr)])
    arr.removeAll()
# SP & MP
arr2 = arcpy.Array()
for x in all:
    for y in x:
        v = y.split(" ")
        if x == we or x == ew:
            pt = arcpy.Point(v[0],v[1])
        else:
            pt = arcpy.Point(v[1],v[0])
        arr.add(pt)
    arr2.add(arr)
    ic.insertRow([arcpy.Polyline(arr)])  
    arr.removeAll()
ic.insertRow([arcpy.Polyline(arr2)])    
del ic

