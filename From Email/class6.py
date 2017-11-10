import arcpy

gdata = "C:/Users/mpleasan/Desktop/c6/analysis_inputs.gdb/indata/"

arcpy.env.workspace = gdata
arcpy.env.overwriteOutput = True

gfcs = arcpy.ListFeatureClasses() # This gets list of all feature classes in environment: Indata

# Save this
if gfcs: # checks to see if list variable gfcs is empty
    print "Yes"
    for g in gfcs: # if it's not empty, this loops through the environment deleting files
       arcpy.Delete_management(g)

ver = "Verified"

proj = "NAD_1983_HARN_Albers"

vgdb = "C:/Users/mpleasan/Desktop/c6/vendor.gdb"

for root, dirs, files in arcpy.da.Walk(vgdb, "FeatureClass"): #Set up walk to gather files
    arcpy.env.workspace = root # Sets environment to the root iterating variable
    for f in files: #sets up loop to go through file
        desc = arcpy.Describe(f) # creates a describe object for the current file 
        if desc.shapeType == "Polygon" or desc.shapeType == "Polyline": #checks if the file is a polygon or polyline
            for x in desc.Fields: # Fields is a **list** of field objects in the describe object. To access them, use dot notation
                if x.name == ver and x.length == 3 and desc.spatialReference.name == proj: #accessing name & length, both properties of the **field object**!!!! Also checks name of spatial reference
                    arcpy.CopyFeatures_management(f, gdata + "my" + f) # if f passes all the above tests, then this copies it to gdata
        elif desc.shapeType == "Point":
            result = arcpy.GetCount_management(f)
            count = int(result.getOutput(0))
            if count == 1:
                arcpy.CopyFeatures_management(f, gdata + "my" + f)

res = "C:/Users/mpleasan/Desktop/c6/results.gdb/"

arcpy.env.workspace = ""

if res: # checks to see if list variable res is empty
    print "Yes"
    for r in res: # if it's not empty, this loops through the environment deleting files
       arcpy.Delete_management(r)

arcpy.env.workspace = gdata

