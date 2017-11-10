import arcpy

arcpy.env.overwriteOutput = True

# Note - next two statements below should reflect where your data is.
rootD=arcpy.env.workspace = "C:\\Users\\sreader\\Dropbox\\pgis_fall2017\\class3i\\c5\\infolder"
out = "C:\\Users\\sreader\\Dropbox\\pgis_fall2017\\class3i\\c5\\outfolder\\out.gdb\\outdata\\"

for root, dirs, files in arcpy.da.Walk(rootD,datatype='FeatureClass'):
    arcpy.env.workspace = root
    for i,f in enumerate(files):
        desc = arcpy.Describe(f)
        if desc.shapeType == "Polygon": bufd = 200
        elif desc.shapeType == "Polyline": bufd = 300
        elif desc.shapeType == "Multipoint": bufd = 500
        bdis = str(bufd) + " Meters"
        arcpy.Buffer_analysis(f, out+"BUF"+str(i+1), bdis, "FULL", "ROUND", "ALL", "")
        fldnames=[]
        [fldnames.append(z.Name) for z in desc.Fields]
        if not "Checked" in fldnames:
            arcpy.AddField_management(f,"Checked","TEXT", "#","#",3)

    