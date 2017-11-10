import arcpy

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
    arcpy.SetParameterAsText(4, "finalout")