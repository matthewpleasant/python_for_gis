import arcpy

def coords(txt, sep, bd):
    wksp = arcpy.env.workpace = "C:/Users/mpleasan/Desktop/Assign9_Nov7/c11ex2.gdb/manatee/"
    arcpy.env.overwriteOutput = "True"
    file = open(txt, 'r')
    arcpy.CreateFeatureclass_management(wksp, "new_coords", "POINT")
    ic = arcpy.da.InsertCursor(wksp + "new_coords", ['SHAPE@X', "SHAPE@Y"])
    for r in file:
        r = r.split(sep)
        r[1] = r[1].replace('\n', '')
        myPoint = (r[0],r[1])
        ic.insertRow(myPoint)
    file.close()
    del ic
    out = []
    for b in bd:
        buffDist = str(b) + " Meters"
        arcpy.Buffer_analysis(wksp + "new_coords", wksp + "new_coordsBuff" + str(b), buffDist, "FULL", "ROUND", "ALL", "#", "PLANAR")
        out.append("new_coordsBuff" + str(b))
    print out
    return out


def buff(bDist, out):
    arcpy.env.workspace = "C:/Users/mpleasan/Desktop/Assign9_Nov7/c11ex2.gdb/manatee/"
    lines = arcpy.ListFeatureClasses("*", "Polyline")
    for b in bDist:
        for o in out:
            vt = arcpy.ValueTable()
            vt.addRow(o)
            for l in lines:
                arcpy.Buffer_analysis(l, l + "buff" + str(b), str(b) + " Meters", "FULL", "ROUND", "ALL", "#", "PLANAR")
                vt.addRow(l + "buff" + str(b))
            print vt
            arcpy.Intersect_analysis(vt, o + "lines" + str(b))