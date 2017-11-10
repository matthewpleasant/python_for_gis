import arcpy, os

wsp = "C:/Users/mpleasan/Desktop/a4/"
indata = wsp + "infolder/"
outdata = wsp + "outfolder/out.gdb/outdata/"

# Cleans out old data from outdata folder, if any exists
arcpy.env.workspace = outdata
out = arcpy.ListFeatureClasses()
if out:
    for file in out:
        arcpy.Delete_management(file)
# end

arcpy.env.workspace = wsp

allfcs = []

for ws, dir, files in arcpy.da.Walk(indata):
    arcpy.env.workspace = ws
    newfiles = [ os.path.join(ws, f) for f in files ]
    allfcs = allfcs + newfiles

for i, f in enumerate(allfcs):
    desc = arcpy.Describe(f)
    if desc.shapeType == "Polygon": bdis = "200 meters"
    elif desc.shapeType == "Polyline": bdis = "300 meters"
    elif desc.shapeType == "Multipoint": bdis = "500 meters"
    arcpy.Buffer_analysis(f, outdata+"buf"+str(i), bdis, "FULL", "ROUND", "ALL", "")
    names = []
    names = [names.append(field.Name) for field in desc.Fields]
    if not "Checked" in names:
            arcpy.AddField_management(f, "Checked", "TEXT", "#", 3)