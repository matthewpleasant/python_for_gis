import arcpy

arcpy.env.overwriteOutput = True

work = "D:\\Dropbox\\pgis_fall2017\\Assignment5\\partB.gdb"
res = "D:\\Dropbox\\pgis_fall2017\\Assignment5\\ptBresults.gdb\\"
temp = "D:\\Dropbox\\pgis_fall2017\\Assignment5\\ptBtemp.gdb\\"

arcpy.env.workspace = res
fcs = arcpy.ListFeatureClasses()
if fcs:
   for f in fcs:
        arcpy.Delete_management(f)

arcpy.env.workspace = work

landfcs = []
fcs = arcpy.ListFeatureClasses("LAND*","Polygon")
for f in fcs:
    d = arcpy.Describe(f).Fields
    for x in d:
        if x.name == "DATA2015":
            landfcs.append(f)
print landfcs           
arcpy.Merge_management(landfcs, temp+"GOODLAND", "")
arcpy.Dissolve_management(temp+"GOODLAND", temp+"GOOD_D", "", "", "MULTI_PART", "DISSOLVE_LINES")

pointfcs = []
fcs = arcpy.ListFeatureClasses("*","Point")
for f in fcs:
    d = arcpy.Describe(f)
    cnt = arcpy.GetCount_management(f)
    if d.shapeType == 'Point' and int(cnt.getOutput(0)) <= 10:
        pointfcs.append(f)
print pointfcs
arcpy.Merge_management(pointfcs, temp+"GOODPTS","")

habvalues = [3,6,7,8]
ptbufs = [1250,1500, 1750]
linebufs = [750, 1000, 1250]

for i in habvalues:
    sql1 = "grid_code = " + str(i)
    arcpy.Select_analysis("habitatsuit", temp+"habitatvalue", sql1)
    for p in ptbufs:
        sql2 = str(p) + " Meters"
        arcpy.Buffer_analysis(temp+"GOODPTS", temp+"PTS_B", sql2, "FULL", "ROUND", "ALL", "", "PLANAR")
        arcpy.Clip_analysis(temp+"GOOD_D", temp+"PTS_B", temp+"GOOD", "")
        for k in linebufs:
            sql3 = str(k) + " Meters"
            arcpy.Buffer_analysis("bikepaths", temp+"bikepathsB", sql3, "FULL", "ROUND", "ALL", "", "PLANAR")
            arcpy.Buffer_analysis("trails", temp+"trailsB", sql3, "FULL", "ROUND", "ALL", "", "PLANAR")
            arcpy.Buffer_analysis("scenic_paths", temp+"scenic_pathsB", sql3, "FULL", "ROUND", "ALL", "", "PLANAR")
            vt = arcpy.ValueTable()
            vt.addRow(temp+"bikepathsB")
            vt.addRow(temp+"trailsB")
            vt.addRow(temp+"scenic_pathsB")
            arcpy.Union_analysis( vt, temp+"LineUnion", "ALL", "", "GAPS")
            a = [1,-1];b=[1,-1];c=[1,-1]
            zz = 0
            for x in a:
                for y in b:
                    for z in c:
                        if x+y+z == 1:
                            sql4 = "FID_bikepathsB = {0} AND FID_scenic_pathsB = {1} AND FID_trailsB = {2}".format(x,y,z)
                            arcpy.Select_analysis(temp+"LineUnion", temp+"LineUnionSel",sql4)
                            arcpy.Clip_analysis(temp+"GOOD", temp+"LineUnionSel", temp+"NEWGOOD", "")
                            arcpy.Clip_analysis(temp+"habitatvalue", temp+"NEWGOOD", temp+"habitatvalueC", "")
                            arcpy.MultipartToSinglepart_management(temp+"habitatvalueC", temp+"singlehabitats")
                            zz = zz+1    
                            name = "H" + str(i) + "P"+str(p) + "L"+str(k)+ "_" + str(zz)
                            arcpy.Clip_analysis("floodzones", temp+"singlehabitats", res+name, "")


