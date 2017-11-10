import arcpy, random

gooddata = "C:/data/class6i/c6/analysis_inputs.gdb/indata/"
arcpy.env.workspace = gooddata
fcs = arcpy.ListFeatureClasses()
if fcs:
    for f in fcs:
        arcpy.Delete_management(f)

v = "Verified"
proj = "NAD_1983_HARN_Albers"
rootD = "C:\\data\\class6i\\c6\\vendor.gdb"

for root, dirs, files in arcpy.da.Walk(rootD,datatype='FeatureClass'):
    arcpy.env.workspace = root
    for i in files:
        d = arcpy.Describe(i)
        if d.shapeType == "Polygon" or d.shapetype == "Polyline":
            for c in d.Fields:
                if c.name == v and c.length == 3 and d.spatialReference.name == proj: 
                    # print d.baseName
                    arcpy.CopyFeatures_management(i, gooddata +  "my" + i)
        elif d.shapeType == "Point":
            cnt = arcpy.GetCount_management(i)
            cnt = int(cnt.getOutput(0))
            if cnt == 1:
                # print d.baseName
                arcpy.CopyFeatures_management(i, gooddata + "my" + i)

res = "C:/data/class6i/c6/results.gdb/"
arcpy.env.workspace = res
fcs = arcpy.ListFeatureClasses()
if fcs:
    for f in fcs:
        arcpy.Delete_management(f)

arcpy.env.overwriteOutput = True
arcpy.env.workspace=gooddata


ptfcs = arcpy.ListFeatureClasses('',"Point")
stnbuf = [2.5,3.0,3.5]
rdsbuf = [1.0,1.5,2.0]
strmbuf = [0.5,1.0,1.5]
npts = [50,75,100]
p1 = 1; p2 = 2; p3=3

nruns = 2
for i in range (1,nruns):
    nstat = random.randint(4,8)
    xx = random.sample(ptfcs,nstat)
    arcpy.Merge_management(xx, "stations_Merge")
    rbuf = random.choice(rdsbuf)
    sbuf = random.choice(strmbuf)
    rbufout = str(rbuf).replace(".","")
    sbufout = str(sbuf).replace(".","")
    rbuffer = str(rbuf) + " Kilometers"
    sbuffer = str(sbuf) + " Kilometers" 
    for n in npts:
        rpts = str(n)
        for s in stnbuf:
            sout = str(s).replace(".","")
            buf1= str(s) + " Kilometers"    
            arcpy.Buffer_analysis("stations_Merge", "stationsBuf", buf1, "FULL", "ROUND", "ALL", "", "PLANAR")
            arcpy.Buffer_analysis("mystreams", "mystreams_Buffer", sbuffer, "FULL", "ROUND", "ALL", "", "PLANAR")
            arcpy.Erase_analysis("stationsBuf", "mystreams_Buffer", "stationsErase1", "")
            arcpy.Buffer_analysis("myroads", "myroads_Buffer", rbuffer, "FULL", "ROUND", "ALL", "", "PLANAR")
            arcpy.Erase_analysis("stationsErase1", "myroads_Buffer", "stationsErase", "") 
            arcpy.Clip_analysis("mysoildrain", "stationsErase", "mysoildrainClip", "")
            arcpy.Dissolve_management("mysoildrainClip", "mysoildrainDiss", "DRAINAGECL", "", "MULTI_PART", "DISSOLVE_LINES")
            arcpy.Clip_analysis("myhabsuit", "stationsErase", "myhabsuitClip", "")
            arcpy.Dissolve_management("myhabsuitClip", "myhabsuitDiss", "Suitability", "", "MULTI_PART", "DISSOLVE_LINES")
            arcpy.Clip_analysis("mybasins", "stationsErase", "mybasinsClip", "")
            arcpy.Dissolve_management("mybasinsClip", "mybasinsDiss", "BASIN", "", "MULTI_PART", "DISSOLVE_LINES")
            vt = arcpy.ValueTable(2)
            vt.addRow("'mysoildrainDiss" + "' " + str(p1))
            vt.addRow("'myhabsuitDiss" + "' " + str(p2))
            vt.addRow("'mybasinsDiss" + "' " + str(p3)) 
            ustring = "mysoildrainDiss " + str(p1) + ";myhabsuitDiss " + str(p2) + ";mybasinsDiss " + str(p3)
            ulist = [["mysoildrainDiss", p1],["myhabsuitDiss", p2],["mybasinsDiss", p3]]
            arcpy.Union_analysis(ustring, "sampling_space", "NO_FID", "", "GAPS")
            arcpy.CreateRandomPoints_management(gooddata, "x1", "", "sampling_space", rpts, "100 Meters", "POINT", "0")
            ostring = "Stn_"+ str(nstat) + "_" + sout + "_" + rpts + "pts" + "_Rds_" + rbufout + "_Strm_" + sbufout 
            if arcpy.Exists(ostring):
                ostring = ostring + "_Duplicate_" + str(i)
            arcpy.Intersect_analysis("x1 #; sampling_space #", res+ostring, "NO_FID", "", "POINT")
            pipnbr = arcpy.GetCount_management(res+ostring)
            pipnbr = int(pipnbr.getOutput(0))
            pstring = str(nstat) + " Stations with Buffer " + sout + ", " + rpts + " points," + "\n" + "Road Buffer of " + rbufout + ", Stream Buffer of " + sbufout + " is:" + "\n" + str(pipnbr)
            print "The number of sample points in the sampling space for: " + "\n" + pstring 

arcpy.env.workspace = res
fcs = arcpy.ListFeatureClasses()
arcpy.Merge_management(fcs, "allpoints")
