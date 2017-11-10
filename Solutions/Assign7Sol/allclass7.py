import arcpy, random
path1 ="D:/Dropbox/pgis_fall2017/Assignment7/"
arcpy.env.workspace = path1 + "working"
fcs = arcpy.ListFeatureClasses()
if fcs:
    for f in fcs:
        arcpy.Delete_management(f)
arcpy.env.workspace = path1 + "original"
fcs = arcpy.ListFeatureClasses()
for f in fcs:
    arcpy.Copy_management(f, path1+"working/"+f)
arcpy.env.workspace = path1+ "working"

#A
flds = ["tractid","PerBlk","SHAPE@XY"]
sc = arcpy.da.SearchCursor("blkgrps.shp",flds)
for row in sc:
    if row[1] > 95 or row[1] < 1:
            print row[0],row[2]
del sc

#B
arcpy.AddField_management("blkgrps.shp","BlackCat","TEXT","","","8")
flds = ["tractid","PerBlk","BlackCat"]
uc = arcpy.da.UpdateCursor("blkgrps.shp",flds)
for row in uc:
        if row[1] > 80:
                row[2] = "High"
        elif row[1] < 10:
                row[2] = "Low"
        else:
                row[2] = "Medium"
        uc.updateRow(row)
del uc

#C
arcpy.CopyFeatures_management("blkgrps.shp","bgs.shp")
flds = ["PerBlk"]
uc = arcpy.da.UpdateCursor("bgs.shp",flds)
for row in uc:
        if row[0] < 1.0:
            uc.deleteRow()
del uc

#D
arcpy.CopyFeatures_management("gas_station.shp","gs.shp")
flds = ["SHAPE@XY","STATION_NA","GRADES","NOZZELS"]
ic = arcpy.da.InsertCursor("gs.shp",flds)
input = open(path1+"newgasstations.txt", "r")
for line in input.readlines():
    v = line.split(",")
    pt = arcpy.Point(v[0],v[1])
    ic.insertRow([pt,v[2],v[3],v[4]])
input.close()
del ic
flds = ["STATION_NA"]
uc = arcpy.da.UpdateCursor("gs.shp",flds)
for row in uc:
    if row[0] == "Sinclair":
        row[0] = "Reader's"
    uc.updateRow(row)

E
arcpy.CreateFeatureclass_management(arcpy.env.workspace,"paths.shp","POLYLINE","","","","gas_station.shp")
arcpy.AddField_management("paths.shp","pathID","TEXT","","","6")
ic = arcpy.da.InsertCursor("paths.shp",["SHAPE@","pathID"])
arr = arcpy.Array()
pt = arcpy.Point(642800,4876000)
arr.add(pt)
input = open(path1+"newgasstations.txt", "r")
i = 1
for line in input.readlines():
    v = line.split(",")
    pt = arcpy.Point(v[0],v[1])
    arr.add(pt)
    pid = "Path"+str(i)
    ic.insertRow([arcpy.Polyline(arr), pid])
    arr.remove(1)
    i = i + 1
input.close()
del ic

F
arcpy.CopyFeatures_management("sareas.shp","newareas.shp")
arr = arcpy.Array()
flds = ["Zone_ID","SHAPE@"]
uc = arcpy.da.UpdateCursor("newareas.shp",flds)
for row in uc:
    if row[0] == "A":
        for y in row[1]:
            for b in y:
                b.X = b.X - 1000
                b.Y = b.Y - 1000
                pt = arcpy.Point(b.X,b.Y)
                arr.add(pt)
        row[1] = arcpy.Polygon(arr)
        uc.updateRow(row)
        arr.removeAll()
    if row[0] == "B":
        for y in row[1]:
            for b in y:
                b.X = b.X + 1000
                b.Y = b.Y - 1000
                pt = arcpy.Point(b.X,b.Y)
                arr.add(pt)
        row[1] = arcpy.Polygon(arr)
        uc.updateRow(row)
        arr.removeAll()
    if row[0] == "C":
        for y in row[1]:
            for b in y:
                b.X = b.X - 1000
                b.Y = b.Y + 1000
                pt = arcpy.Point(b.X,b.Y)
                arr.add(pt)
        row[1] = arcpy.Polygon(arr)
        uc.updateRow(row)
        arr.removeAll()
    if row[0] == "D":
        for y in row[1]:
            for b in y:
                b.X = b.X + 1000
                b.Y = b.Y + 1000
                pt = arcpy.Point(b.X,b.Y)
                arr.add(pt)
        row[1] = arcpy.Polygon(arr)
        uc.updateRow(row)
        arr.removeAll()
del uc

#G
inputFC = "HgValues.shp"
backup = "Hgvaluesv1.shp"
uniqFLD = "UniqueID"
arcpy.CopyFeatures_management(inputFC,backup)
d = {}
flds = ["SHAPE@XY",uniqFLD]
uc = arcpy.da.UpdateCursor(backup,flds)
pntID = 1
for row in uc:
    ptx = row[0][0]
    pty = row[0][1]
    key = str(ptx) + " " + str(pty)
    print key
    if not d.has_key(key):
        d[key] = pntID
        pntID = pntID + 1
    row[1] = d[key]
    uc.updateRow(row)
arcpy.Dissolve_management(backup,"newHg",uniqFLD,"HgValue MEAN","MULTI_PART")
del uc   

H

out = "transects.shp"

arcpy.CreateFeatureclass_management(path1+"working",out,"POLYLINE")
arcpy.AddField_management(out,"Code","TEXT","","","3")
arr = arcpy.Array()
ic = arcpy.da.InsertCursor(out,["SHAPE@","Code"])

codes = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T"]

i = 0
while i < 20:
        x1 = random.randint(0,100)
        y1 = random.randint(0,100)
        p1 = arcpy.Point(x1,y1)
        arr.add(p1)
        x2 = random.randint(0,100)
        y2 = random.randint(0,100)
        p2 = arcpy.Point(x2,y2)
        arr.add(p2)
        line = arcpy.Polyline(arr)
        if line.length >= 35 and line.length <= 55:
            c = codes[i]
            ic.insertRow([line,c])
            i = i+1
        else:
            print "transect not correct length"
        arr.removeAll()
del ic

