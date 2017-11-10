import arcpy
arcpy.env.overwriteOutput = True
w=arcpy.env.workspace = "C:\\data\\A3\\leeton.gdb\\iout"
ipath = w[:-4]
fpath = w[:-4]+"fout\\"

C1A = "M-1";  Z1A = "'M-1'"
C1B = "RES";  Z1B = "'RES'"
C2A = "M-2" 
C2B = "RES" 
C3A = "M-1"
C3B = "O-L"

s1 = "(onleft = '" + C1A + "' AND onright = '" + C1B + "' )OR(onleft = '" + C1B + "' AND onright = '" + C1A + "')"
s2 = "(onleft = '" + C2A + "' AND onright = '" + C2B + "' )OR(onleft = '" + C2B + "' AND onright = '" + C2A + "')"
s3 = "(onleft = '" + C3A + "' AND onright = '" + C3B + "' )OR(onleft = '" + C3B + "' AND onright = '" + C3A + "')"

# s1f = "(onleft = {0} AND onright = {1}) OR (onleft = {1} AND onright = {0})".format(Z1A,Z1B)
# if using Z1A/Z1B, or
# s1f = "(onleft = '{0}' AND onright = '{1}' )OR( onleft = '{1}' AND onright = '{0}')".format(C1A, C1B)

t1 = "LANDUSE = '" + C1A + "' OR LANDUSE = '" + C1B + "'"
t2 = "LANDUSE = '" + C2A + "' OR LANDUSE = '" + C2B + "'"
t3 = "LANDUSE = '" + C3A + "' OR LANDUSE = '" + C3B + "'"

c1 = "conf1"; c2 = "conf2"; c3 = "conf3" 

u1 = c1 + " #;" + c2 + " #;" + c3 + " #"

p1 =1; p2=2; p3=3

u2 = [[c1, p1],[c2,p2],[c3,p3]]

vt = arcpy.ValueTable(2)
vt.addRow(c1 + " " + str(p1))
vt.addRow(c2 + " " + str(p2))
vt.addRow(c3 + " " + str(p3))

arcpy.Dissolve_management(ipath+"landu", "landu_Dissolve", "LANDUSE", "", "MULTI_PART", "DISSOLVE_LINES")

arcpy.Select_analysis(ipath+"landarcs", "m1_res", s1) # or s1f
arcpy.Buffer_analysis("m1_res", "m1_resb", "200 Feet", "FULL", "ROUND", "ALL", "", "PLANAR")
arcpy.Select_analysis(ipath+"landu", "m1_resp", t1)
arcpy.Clip_analysis("m1_resb", "m1_resp", c1, "")

arcpy.Select_analysis(ipath+"landarcs", "res_m2", s2)
arcpy.Buffer_analysis("res_m2", "res_m2b", "125 Feet", "FULL", "ROUND", "ALL", "", "PLANAR")
arcpy.Select_analysis(ipath+"landu", "m2resp", t2)
arcpy.Clip_analysis("res_m2b", "m2resp", c2, "")

arcpy.Select_analysis(ipath+"landarcs", "m1_ol", s3)
arcpy.Buffer_analysis("m1_ol", "m1_olb", "100 Feet", "FULL", "ROUND", "ALL", "", "PLANAR")
arcpy.Select_analysis(ipath+"landu", "m1_olp", t3)
arcpy.Clip_analysis("m1_olb", "m1_olp", c3, "")

# arcpy.Union_analysis("conf1 #;conf2 #;conf3 #", "conunion", "ONLY_FID", "", "GAPS")
# arcpy.Union_analysis(u1, "conunion", "ONLY_FID", "", "GAPS")
# arcpy.Union_analysis(u2, "conunion", "ONLY_FID", "", "GAPS")

u2[0][1] = p2; u2[1][1] = p3; u2[2][1] = p1

arcpy.Union_analysis(u2, "conunion", "ONLY_FID", "", "GAPS")
arcpy.Union_analysis(vt, "conunion", "ONLY_FID", "", "GAPS")
arcpy.Dissolve_management("conunion", "conflict", "", "", "MULTI_PART", "DISSOLVE_LINES")

arcpy.Dissolve_management(ipath+"streams", "riv_diss", "", "", "MULTI_PART", "DISSOLVE_LINES")
arcpy.Buffer_analysis("riv_diss", "riv_buf", "100 Feet", "FULL", "ROUND", "ALL", "", "PLANAR")
arcpy.Select_analysis(ipath+"floods", "flds_Sel", "ZONE_ = 'A' OR ZONE_ = 'B'")
arcpy.Dissolve_management("flds_Sel", "flds_Diss", "", "", "MULTI_PART", "DISSOLVE_LINES")

arcpy.Union_analysis("riv_buf #;flds_Diss #", "riv_fld", "ONLY_FID", "", "GAPS")
arcpy.Dissolve_management("riv_fld", "natural", "", "", "MULTI_PART", "DISSOLVE_LINES")

arcpy.Union_analysis("conflict #;natural #", "both", "ONLY_FID", "", "GAPS")
res1 = arcpy.Intersect_analysis("landu_Dissolve #;both #", fpath+"greenbelt", "NO_FID", "", "INPUT")

print res1.messageCount
print res1.getMessage(5)
print res1.getMessage(0)

res2 = arcpy.GetCount_management(fpath+"greenbelt")
cnt = int(res2.getOutput(0))
print "The number of features in the final output is:   " + str(cnt) 



