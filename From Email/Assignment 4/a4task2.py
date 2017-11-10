import arcpy, os

arcpy.env.overwriteOutput = True

# Note - next two statements below should reflect where your data is.
arcpy.env.workspace = "C:/Users/mpleasan/Desktop/a4/infolder/"
out = "C:/Users/mpleasan/Desktop/a4/outfolder/outdata/"

wslist = arcpy.ListWorkspaces('',"FileGDB")
fldlist = arcpy.ListWorkspaces('',"Folder")

if wslist == []:
    print 'No Geodatabases'
else:
    print "Geodatabases:"
    for ws in wslist:
        print ws

if fldlist == []:
    print 'No Shapefile Folders'
else:
    print "Shapefile Folders:"
    for f in fldlist:
        print f

allws = wslist+fldlist

allfcs =[]

for a in allws:
    arcpy.env.workspace = a
    fcs = arcpy.ListFeatureClasses()
    for i, f in enumerate(fcs):
        fcs[i] = os.path.join(a, f)
    allfcs = allfcs + fcs
    dslist = arcpy.ListDatasets()
    if dslist == []:
        continue
    else:
        for i, d in enumerate(dslist):
            fdfc = arcpy.ListFeatureClasses("","",d)
            for i, f in enumerate(fdfc):
                fdfc[i] = os.path.join(a, d, f)
            allfcs = allfcs + fdfc

##n=1
##for f in allfcs:
##    desc = arcpy.Describe(f)
##    print desc.shapeType
##    if desc.shapeType == "Polygon": bufd = 200
##    elif desc.shapeType == "Polyline": bufd = 300
##    elif desc.shapeType == "Multipoint": bufd = 500
##    bdis = str(bufd) + " Meters"
##    arcpy.Buffer_analysis(f, out+"BUF"+str(n), bdis, "FULL", "ROUND", "ALL", "")
##    fldnames=[]
##    for z in desc.Fields:
##        fldnames.append(z.Name)
##    if not "Checked" in fldnames:
##        arcpy.AddField_management(f,"Checked","TEXT", "#","#",3)
##    n=n+1