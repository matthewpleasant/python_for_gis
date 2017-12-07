import arcpy

filePath=arcpy.env.workspace= "C:/Users/mpleasan/Desktop/A3/A3/leeton.gdb/"

arcpy.env.overwriteOutput = True 

iOut = filePath + "iout/"

fOut = filePath + "fout/"

## Conflict 1 ##
C1A = "M1"
C1B = "RES"
S1 = "(onleft = '" + C1A + "' AND onright = '" + C1B + "' )OR( onleft = '" + C1B + "' AND onright = '" + C1A + "')"
#S1F = "(onleft = '{0}' AND onright = '{1}' )OR( onleft = '{2}' AND onright = '{3}')".format(C1A, C1B, C1B, C1A)
L1 = "LANDUSE = '" + C1A + "' OR " "LANDUSE = '" + C1B + "'"

## Conflict 2 ##
C2A = "M2"
C2B = "RES"
S2 = "(onleft = '" + C2A + "' AND onright = '" + C2B + "' )OR( onleft = '" + C2B + "' AND onright = '" + C2A + "')"
L2 = "LANDUSE = '" + C2A + "' OR " "LANDUSE = '" + C2B + "'"

## Conflict 3 ##
C3A = "M3"
C3B = "RES"
S3 = "(onleft = '" + C3A + "' AND onright = '" + C3B + "' )OR( onleft = '" + C3B + "' AND onright = '" + C3A + "')"
L3 = "LANDUSE = '" + C3A + "' OR " "LANDUSE = '" + C3B + "'"

## Conflict output file names ##

cf1 = "conf1"
cf2 = "conf2"
cf3 = "conf3"

## Union Tool Variable ##

# conflictUnion = filePath + cf1 + " #;" + filePath + cf2 + " #;" + filePath + cf3 + " #"

p1 = 1
p2 = 2
p3 = 3
uList = [ [iOut + cf1, p1], [iOut + cf2, p2], [iOut + cf3, p3] ]

### GEOPROCESSING BEGINS ####

# Process: Dissolve (5)
# Dissolves the landu shape file using the "LANDUSE" field, outputs the file "landu_Dissolve"
# Output: landu_Dissolve in iout
arcpy.Dissolve_management(filePath + "landu", iOut + "landu_Dissolve", "LANDUSE", "", "MULTI_PART", "DISSOLVE_LINES")

############ CONFLICT DESIGNATION 1 

# Process: Select (2)
# Selects lines from the landarcs layer where the "onleft" field equals 'M-1' and onright equals 'RES' and vice versa
# Query: "(onleft = 'M-1' AND onright = 'RES' )OR( onleft = 'RES' AND onright = 'M-1')"
# Output: M1RES in iout
arcpy.Select_analysis(filePath + "landarcs", iOut + C1A + C1B, S1)

# Process: Buffer (2)
# Buffers 200 feet around the lines selected above from landarcs
# Output: m1_resb in iout
arcpy.Buffer_analysis(filePath + C1A + C1B, iOut + "m1_resb", "200 Feet", "FULL", "ROUND", "ALL", "", "PLANAR")

# Process: Select (5)
# Selects from landu layer all features with "LANDUSE" field equal to M-1 or RES
# Output: m1_resp
arcpy.Select_analysis(filePath + "landu", iOut + "m1_resp", L1)

# Process: Clip
# Clips from the land use selection above (m1_resb) using the buffers created above (m1_resp)
# Output: conf1 in iout
arcpy.Clip_analysis(filePath + "m1_resb", iOut + "m1_resp", iOut + cf1, "")

########## CONFLICT DESIGNATION 2

# Process: Select (3)
# Selects from landarcs all features where onleft field equals "M-2" and onright equals "RES" and vice versa
# Out: res_m2 in iOut
arcpy.Select_analysis(filePath + "landarcs", iOut + C2A + C2B, S2)

# Process: Buffer (3)
# Buffers 125 feet around features selected above from landarcs
# Output: res_m2b in iout
arcpy.Buffer_analysis(filePath + "res_m2", iOut + "res_m2b", "125 Feet", "FULL", "ROUND", "ALL", "", "PLANAR")

# Process: Select (6)
arcpy.Select_analysis(filePath + "landu", iOut + "m2resp", L2)

# Process: Clip (2)
arcpy.Clip_analysis(filePath + "res_m2b", iOut + "m2resp", iOut + cf2, "")

######### CONFLICT DESIGNATION 3 

# Process: Select (4)
arcpy.Select_analysis(filePath + "landarcs", iOut + C3A + C3B, S3)

# Process: Buffer (4)
arcpy.Buffer_analysis(filePath + "m1_ol", iOut + "m1_olb", "100 Feet", "FULL", "ROUND", "ALL", "", "PLANAR")

# Process: Select (7)
arcpy.Select_analysis(filePath + "landu", iOut + "m1_olp", L3)

# Process: Clip (3)
arcpy.Clip_analysis(filePath + "m1_olb", iOut + "m1_olp", iOut + cf3, "")

########## END OF CONFLICT DESIGNATIONS

# Process: Union (2)
#arcpy.Union_analysis(conflictUnion, iOut + conunion, "ONLY_FID", "", "GAPS")
arcpy.Union_analysis(uList, iOut + "conunion", "ONLY_FID", "", "GAPS")

uList[0][1] = p2
uList[1][1] = p3
uList[2][1] = p1

arcpy.Union_analysis(uList, iOut + "conunion", "ONLY_FID", "", "GAPS")

vtab = arcpy.ValueTable(2)

vtab.addRow(cf1 + " " + str(p1))
vtab.addRow(cf2 + " " + str(p2))
vtab.addRow(cf3 + " " + str(p3))

arcpy.Union_analysis(vtab, iOut + "conunion", "ONLY_FID", "", "GAPS")

# Process: Dissolve (4)
arcpy.Dissolve_management(filePath + "conunion", iOut + "conflict", "", "", "MULTI_PART", "DISSOLVE_LINES")

#Process: Dissolve
arcpy.Dissolve_management(filePath + "streams", iOut + "riv_diss", "", "", "MULTI_PART", "DISSOLVE_LINES")

# Process: Buffer
arcpy.Buffer_analysis(filePath + "riv_diss", iOut + "riv_buf", "100 Feet", "FULL", "ROUND", "ALL", "", "PLANAR")

# Process: Select
arcpy.Select_analysis(filePath + "floods", iOut + "flds_Sel", "ZONE_ = 'A' OR ZONE_ = 'B'")

# Process: Dissolve (2)
arcpy.Dissolve_management(filePath + "flds_Sel", iOut + "flds_Diss", "", "", "MULTI_PART", "DISSOLVE_LINES")

# Process: Union
arcpy.Union_analysis(filePath + "riv_buf #;" + filePath + "flds_Diss #", iOut + "riv_fld", "ONLY_FID", "", "GAPS")

# Process: Dissolve (3)
arcpy.Dissolve_management(filePath + "riv_fld", iOut + "natural", "", "", "MULTI_PART", "DISSOLVE_LINES")

# Process: Union (3)
arcpy.Union_analysis(filePath + "conflict #;" + filePath + "natural #", iOut  + "both", "ONLY_FID", "", "GAPS")

# Process: Intersect
res1 = arcpy.Intersect_analysis(iOut + "landu_Dissolve #;" + iOut + "both #", fOut + "greenbelt", "NO_FID", "", "INPUT")

print "Number of messages in output: " + str(res1.messageCount)
print "Fifth message of output: " + res1.getMessage(4)
print "Input feature class: " + res1.getInput(0)
print "Output feature class location: " + res1.getOutput(0)
print "Number of features in final output: " + str(arcpy.GetCount_management(res1))