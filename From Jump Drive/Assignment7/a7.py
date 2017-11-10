import arcpy, random
# edit path1 variable below to reflect where your data is

path1 ="C:/Users/mpleasan/Desktop/Assignment7/"
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

##sc = arcpy.da.SearchCursor("blkgrps.shp", ["tractid", "PerBlk", "SHAPE@XY"])
##
##for r in sc:
##    if r[1] > 95 or r[1] < 0.5:
##        print "Census Tract: " + r[0], "Centroid: " + str(r[2][0]) + ", " + str(r[2][1]), "Percentage: " + str(r[1])
##
##del sc    

#B

##arcpy.AddField_management("blkgrps.shp", "Level", "Text", "#", "#", "8")
##
##uc = arcpy.da.UpdateCursor("blkgrps.shp", ["PerBlk", "Level"])
##
##for r in uc:
##    if r[0] > 80:
##        r[1] = "High"
##        uc.updateRow(r)
##    elif r[0] < 10:
##        r[1] = "Low"
##        uc.updateRow(r)
##    else:
##        r[1] = "Medium"
##        uc.updateRow(r)

#C

##arcpy.CopyFeatures_management("blkgrps.shp", "blkgrps_copy.shp")
##
##uc = arcpy.da.UpdateCursor("blkgrps_copy.shp", ["PerBlk"])
##
##for r in uc:
##    if r[0] < 25:
##        uc.deleteRow()

#D

##arcpy.CopyFeatures_management("gas_station.shp", "gas_station_copy")
##input = file("C:/Users/mpleasan/Desktop/Assignment7/newgasstations.txt", "r")
##fields = ["SHAPE@", "STATION_NA", "GRADES", "NOZZELS"]
##
##ic = arcpy.da.InsertCursor("gas_station_copy.shp", fields)
##uc = arcpy.da.UpdateCursor("gas_station_copy.shp", "STATION_NA")
##newstations = []
##
##for r in input:
##    l = r.split(",")
##    l[4] = l[4].replace("\n", "")
##    newstations.append(l)
##
##for s in newstations:
##    point = arcpy.PointGeometry(arcpy.Point(s[0], s[1]))
##    ic.insertRow([point, s[2], s[3], s[4]])
##
##for r in uc:
##    if r[0] == "Sinclair":
##        r[0]= "Reader's"
##        uc.updateRow(r)
##    
##del ic
##del uc

#E

##arcpy.CreateFeatureclass_management(path1 + "working", "gas_lines", "POLYLINE", "#", "DISABLED", "DISABLED", "C:/Users/mpleasan/Desktop/Assignment7/original/gas_station.prj")
##arcpy.AddField_management("gas_lines.shp", "LINE_NA", "TEXT", "#", "#", "6")
##input = file("C:/Users/mpleasan/Desktop/Assignment7/newgasstations.txt", "r")
##
##end = arcpy.Point(float(642800),float(4876000))
##path_num = 1
##arr = arcpy.Array()
##ic = arcpy.da.InsertCursor("gas_lines.shp", ["Shape@", "LINE_NA"])
##
##for r in input:
##    l = r.split(",")
##    start = arcpy.Point(float(l[0]), float(l[1]))
##    arr.add(start)
##    arr.add(end)
##    ic.insertRow([arcpy.Polyline(arr), "path" + str(path_num)])
##    path_num = path_num + 1
##
##del ic
##

#F

arcpy.CopyFeatures_management("sareas.shp", "sareas_copy")

uc = arcpy.da.UpdateCursor("sareas_copy.shp", ["SHAPE@", "Zone_ID"])

arr = arcpy.Array()

for r in uc:
    if r[1] == "A":
        for q in r[0]:
            for s in q:
                s.X = s.X - 1000
                s.Y = s.Y - 1000
                pt = arcpy.Point(s.X, s.Y)
                arr.add(pt)
            polygon = arcpy.Polygon(arr)
            r[0] = polygon
            uc.updateRow(r)
            arr = arcpy.Array()
    if r[1] == "B":
        for q in r[0]:
            for s in q:
                s.X = s.X + 1000
                s.Y = s.Y - 1000
                pt = arcpy.Point(s.X, s.Y)
                arr.add(pt)
            polygon = arcpy.Polygon(arr)
            r[0] = polygon
            uc.updateRow(r)
            arr = arcpy.Array()
    if r[1] == "C":
        for q in r[0]:
            for s in q:
                s.X = s.X - 1000
                s.Y = s.Y + 1000
                pt = arcpy.Point(s.X, s.Y)
                arr.add(pt)
            polygon = arcpy.Polygon(arr)
            r[0] = polygon
            uc.updateRow(r)
            arr = arcpy.Array()
    if r[1] == "D":
        for q in r[0]:
            for s in q:
                s.X = s.X + 1000
                s.Y = s.Y + 1000
                pt = arcpy.Point(s.X, s.Y)
                arr.add(pt)
            polygon = arcpy.Polygon(arr)
            r[0] = polygon
            uc.updateRow(r)
            arr = arcpy.Array()
del uc