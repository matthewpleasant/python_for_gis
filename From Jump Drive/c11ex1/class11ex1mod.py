import arcpy, assignNine
# note that the statement below can be omitted once a script tool and the
# environment setting of the map doc used

arcpy.env.overwriteOutput = 1

# the following will come from the script tool ultimately but we can
# define some values to use here for sake of development

wksp = arcpy.env.workspace = 'C:/Users/mpleasan/Desktop/c11ex1.gdb/manatee'

lfc = ["rail", "stream"]
bd = 100
bdunits = "Meters"
flood = "flzone"
fld1 = "SFHA"
fldval = "IN"

fc1 = "landuse"
fld2 = "DESCRIPT"

# Start with the statement to start the function definition for function 1

def firstFunction(wksp, lfc, bd, bdunits, flood, fld1, fldval):
    polygons = []
    buffDis = str(bd) + " " + bdunits
    for x in lfc:
        arcpy.Buffer_analysis(x, x+"buff", buffDis, "FULL", "ROUND", "ALL", "")
        q = fld1 + " = '" + fldval + "'"
        poly = arcpy.Select_analysis("flzone", "polysel", q)
        polygons.append("polysel")
        vt = arcpy.ValueTable(2)
        bfcs = arcpy.ListFeatureClasses("*buff*", "Polygon")
        for f in bfcs:
            vt.addRow(f)
        oname = "cliparea"
        arcpy.Union_analysis(vt, "out", "ALL", "", "GAPS")
        arcpy.Dissolve_management("out", oname, "", "", "MULTI_PART", "DISSOLVE_LINES")
        return oname

def functionTwo(fc1, fc2, fld):
    arcpy.Dissolve_management(fc1, "fc1D", fld, "", "MULTI_PART", "DISSOLVE_LINES")
    arcpy.Clip_analysis("fc1D", fc2, "finalout", "")

out = assignNine.firstFunction(wksp, lfc, bd, bdunits, flood, fld1, fldval)
assignNine.functionTwo("C:/Users/mpleasan/Desktop/c11ex1/c11ex1.gdb/landuse", out, 'DESCRIPT')