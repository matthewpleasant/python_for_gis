import arcpy

arcpy.env.overwriteOutput = True

# Note - next two statements below should reflect where your data is.
arcpy.env.workspace = "C:\\Users\\sreader\\Dropbox\\pgis_fall2017\\class3i\\c5\\infolder"
out = "C:\\Users\\sreader\\Dropbox\\pgis_fall2017\\class3i\\c5\\outfolder\\out.gdb\\outdata\\"

allws = arcpy.ListWorkspaces()
allfcs =[]

for a in allws:
    arcpy.env.workspace = a
    fcs = arcpy.ListFeatureClasses()
    i = 0
    for f in fcs:
        fcs[i] = a+"\\"+ f
        i = i+1
    allfcs = allfcs + fcs
    dslist = arcpy.ListDatasets()
    if dslist == []:
        continue
    else:
        for d in dslist:
            fdfc = arcpy.ListFeatureClasses("","",d)
            i = 0
            for f in fdfc:
                fdfc[i] = a + "\\" + d + "\\" + f
                i=i+1
            allfcs = allfcs + fdfc

n=1
for f in allfcs:
    desc = arcpy.Describe(f)
    if desc.shapeType == "Polygon": bufd = 200
    elif desc.shapeType == "Polyline": bufd = 300
    elif desc.shapeType == "Multipoint": bufd = 500
    bdis = str(bufd) + " Meters"
    arcpy.Buffer_analysis(f, out+"BUF"+str(n), bdis, "FULL", "ROUND", "ALL", "")
    fldnames=[]
    for z in desc.Fields:
        fldnames.append(z.Name)
    if not "Checked" in fldnames:
        arcpy.AddField_management(f,"Checked","TEXT", "#","#",3)
    n=n+1
    