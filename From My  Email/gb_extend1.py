import arcpy
arcpy.env.overwriteOutput=True

out = "C:\\users\\sreader\\Dropbox\\pgis_fall2017\\class10i\\d1\\outputs\\"

zone = arcpy.GetParameterAsText(0)
rbuf = arcpy.GetParameter(1)
cbuf = arcpy.GetParameterAsText(2)
out = arcpy.GetParameterAsText(3) + "\\"
in1 = arcpy.GetParameter(4)
zz = arcpy.GetParameter(5)

arcpy.AddMessage(in1)
arcpy.AddMessage(type(out))

arcpy.env.workspace = in1


zone = zone.split(";")
zone = [ i.replace("'","") for i in zone ]
arcpy.AddMessage(zone)

cbuf = cbuf.split(";")
cbuf = [i.split(" ") for i in cbuf]

arcpy.AddMessage(cbuf)
arcpy.AddMessage(type(cbuf))

#cdist = [["300", "200", "150"],["400", "250", "200"], ["500","300","250"]]
s = 1
outlist = []
arcpy.Dissolve_management("streams", "streamsD", "", "", "MULTI_PART", "DISSOLVE_LINES")
arcpy.Dissolve_management("landu", "landuD", "LANDUSE", "", "MULTI_PART", "DISSOLVE_LINES")
for zn in zone:
    if zn == "Zone A":
        arcpy.Select_analysis("floods", "floods_Select", "ZONE_ = 'A'")
    elif zn == "Zone A and B":
        arcpy.Select_analysis("floods", "floods_Select", "ZONE_ = 'A' OR ZONE_ = 'B'")
    arcpy.Dissolve_management("floods_Select", "floods_Dissolve", "", "", "MULTI_PART", "DISSOLVE_LINES")
    for riv in rbuf:
        bufd = str(riv) + " Feet"
        arcpy.Buffer_analysis("streamsD", "streamsB", bufd, "FULL", "ROUND", "ALL", "")
        arcpy.Union_analysis("streamsB #; floods_Dissolve #","streams_floods", "ONLY_FID", "", "GAPS")
        arcpy.Dissolve_management("streams_floods", "natural", "", "", "MULTI_PART", "DISSOLVE_LINES")
        for conf in cbuf:
            c1 = conf[0] + " Feet"
            c2 = conf[1] + " Feet"
            c3 = conf[2] + " Feet"
            arcpy.Select_analysis("landarcs", "m1_res", "(onleft = 'M-1' AND onright = 'RES') OR (onleft = 'RES' AND onright = 'M-1')")
            arcpy.Select_analysis("landarcs", "res_m2", "(onleft = 'M-2' AND onright = 'RES') OR (onleft = 'RES' AND onright = 'M-2')")
            arcpy.Select_analysis("landarcs", "m1_ol", "(onleft = 'M-1' AND onright = 'O-L' ) OR (onleft = 'O-L' AND onright = 'M-1')")
            arcpy.Buffer_analysis("m1_res", "m1_resb", c1, "FULL", "ROUND", "ALL", "")
            arcpy.Buffer_analysis("res_m2", "res_m2b", c2, "FULL", "ROUND", "ALL", "")
            arcpy.Buffer_analysis("m1_ol", "m1_olb", c3, "FULL", "ROUND", "ALL", "")
            arcpy.Select_analysis("landu", "m1_resp", "LANDUSE = 'M-1' OR LANDUSE = 'RES'")
            arcpy.Select_analysis("landu", "m2resp", "LANDUSE = 'M-2' OR LANDUSE = 'RES'")
            arcpy.Select_analysis("landu", "m1_olp", "LANDUSE = 'O-L' OR LANDUSE = 'M-1'")
            arcpy.Clip_analysis("m1_resb", "m1_resp", "conf1", "")
            arcpy.Clip_analysis("res_m2b", "m2resp", "conf2", "")
            arcpy.Clip_analysis("m1_olb", "m1_olp", "conf3", "")
            arcpy.Union_analysis("conf1 #;conf2 #;conf3 #", "conunion", "ONLY_FID", "", "GAPS")
            arcpy.Dissolve_management("conunion", "conflict", "", "", "MULTI_PART", "DISSOLVE_LINES")
            if zz:
                arcpy.Union_analysis("conflict #;natural #", "both", "ONLY_FID", "", "GAPS")
                arcpy.AddMessage("UNION")
            else:
                arcpy.Intersect_analysis("conflict #;natural #", "both", "ONLY_FID", "", "INPUT")
                arcpy.AddMessage("INERSECT")
            outstring = out+"greenbelt"+str(s)+".shp"
            arcpy.Intersect_analysis("both #;landuD #", outstring, "NO_FID", "", "INPUT")
            outlist.append(outstring)
            s=s+1

res = ";".join(outlist)
arcpy.SetParameterAsText(6, res)