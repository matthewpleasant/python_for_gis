import arcpy, assignNine
reload(assignNine)
# note that the statement below can be omitted once a script tool and the
# environment setting of the map doc used

arcpy.env.overwriteOutput = 1

# the following will come from the script tool ultimately but we can
# define some values to use here for sake of development

lfc = arcpy.GetParameter(0)
arcpy.AddMessage(lfc)
#Ex: ["rail", "stream"]

bd = arcpy.GetParameterAsText(1)
arcpy.AddMessage(bd)
#100

bdunits = arcpy.GetParameterAsText(2)
arcpy.AddMessage(bdunits)
# Ex: "Meters"

fldval = arcpy.GetParameterAsText(3)
arcpy.AddMessage(fldval)

## DEFAULT PARAMETERS ##
wksp = arcpy.env.workspace = 'C:/Users/mpleasan/Desktop/c11ex1.gdb/manatee'
fc1 = "landuse"
fld2 = "DESCRIPT"
flood = "flzone"
fld1 = "SFHA"

out = assignNine.firstFunction(wksp, lfc, bd, bdunits, flood, fld1, fldval)
assignNine.functionTwo("C:/Users/mpleasan/Desktop/c11ex1/c11ex1.gdb/landuse", out, 'DESCRIPT')