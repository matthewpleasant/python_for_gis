# I'll give you the first statement because I am SUCH a nice guy! ;)
import arcpy
# set the property to over write any outputs
arcpy.env.overwriteOutput = True

# create three string variables and set each one to one of the three gdb's you will use

input = "C:/Users/mpleasan/Desktop/a5partB/partB.gdb/"
output = "C:/Users/mpleasan/Desktop/a5partB/ptBtemp.gdb/"
res = "C:/Users/mpleasan/Desktop/a5partB/ptBresults.gdb/"

# set the workspace to the ptBresults.gdb and then test for existence of feature classes
# there and delete any found

arcpy.env.workspace = res
fcs = arcpy.ListFeatureClasses()
if fcs:
    print "Deleting feature classes in ptBresults..."
    for f in fcs:
        arcpy.Delete_management(f)

# set the workspace back to partB.gdb

arcpy.env.workspace = input

# in this section of code you need to FIND the polygon feature classes that will be merged - see instructions -
# and then merge them and dissolve to produce the area that is 'good land' - see model graphic
# tip: start with empty list
# tip: think listing of feature classes and how you can restrict the listing
# tip: use of Describe
# tip: use print statement to verify you have 4 (hopefully correct!) feature classes before merging

gfcs = []

polyfiles = arcpy.ListFeatureClasses("LAND*", "Polygon")
for p in polyfiles:
    desc = arcpy.Describe(p)
    for f in desc.Fields:
        files = []
        if f.name == "DATA2015":
            files.append(p)
        gfcs = gfcs + files

arcpy.Merge_management(gfcs, output + "GOODLAND")

# in this section of code you need to FIND the point feature classes that will be merged
# and then merge them to produce the good points (field stations) - see model graphic
# tip: start with empty list
# tip: think listing of feature classes and how you can restrict the listing
# note that there is a difference when it comes to points between 'feature type' and 'shape type'
# tip: use of Describe
# tip: think tool to give you the number of features
# tip: use print statement to verify you have 2 (hopefully correct!) feature classes before merging

point = []

pointfiles = arcpy.ListFeatureClasses("*", "Point")

for f in pointfiles:
    des = arcpy.Describe(f)
    if des.shapeType == "Point":   
        x = arcpy.GetCount_management(f)
        x = int(x.getOutput(0))
        ptfcs = []
        if x <= 10:
            ptfcs.append(f)
            point = point + ptfcs

arcpy.Merge_management(point, output + "GOODPTS", "")

# in this section of code, you will create the lists of values needed for looping
# you need to create lists for habitat scores, point buffer values  and line buffer values - see instructions
# tip: create 3 extra lists with just one value that you can use while developing - see instruction tips
# tip: comment out your real lists and use the extra ones while developing


##habitatScores = [3, 6, 7, 8]
##pointBuffers = [1250, 1500, 1750]
##lineBuffers = [750, 1000, 1250]

hS = [3]
pB = [1250]
lB = [750,1000,1250]



pairs = [ [1,'"Type" = \'Scenic_Path\' AND "SURFACE" = \'TRAIL\' AND NOT "DESCRIPT" = \'BikePath\''],
          [2,'"Type" = \'Scenic Path\' AND "DESCRIPT" = \'BikePath\' AND NOT "SURFACE" = \'TRAIL\''],
          [3,'"DESCRIPT" = \'BikePath\' AND "SURFACE" = \'TRAIL\' AND NOT "TYPE" = \'Scenic Path\''] ]


# OK, so now we are into the 'nitty-gritty'!
# you need to develop your looping structures here - see instructions
# and then slot in the right tools at the right places vis-a-vis the model
# the particularly tricky part is the last looping structure (actually structures!) when you
# need to select the 2 from 3 line buffers - see instructions

a=[1,-1]
b2=[1,-1]
c=[1,-1]

for s in hS:                          #STARTS LOOP WITH FIRST HABITAT SCORE
    arcpy.Select_analysis("habitatsuit", output + "habitatvalue", "grid_code= " + str(s)) # SELECTS ALL LAND WITH HABITAT SCORE 3, OUTPUT FILE HAS "HABITATVALUE"
    for b in pB:                      # STARTS POINT BUFFER LOOP       
        arcpy.Buffer_analysis(output + "GOODPTS", output + "PTS_B", str(b) + "  Meters", "FULL", "ROUND", "ALL", "", "PLANAR")
        for l in lB:                  # STARTS LINE BUFFER LOOP
            arcpy.Buffer_analysis("scenic_paths", output + "scenic_pathsB", str(l) + " Meters", "FULL", "ROUND", "ALL", "", "PLANAR")
            arcpy.Buffer_analysis("trails", output + "trailsB", str(l) + " Meters", "FULL", "ROUND", "ALL", "", "PLANAR")
            arcpy.Buffer_analysis("bikepaths", output + "bikepathB", str(l) + " Meters", "FULL", "ROUND", "ALL", "", "PLANAR")
            arcpy.Union_analysis([output + "scenic_pathsB", output + "trailsB", output + "bikepathB"], output + "LineUnion", "ALL", "", "GAPS")
            for x in a:
                for y in b2:
                    for z in c:
                        if x + y + z == 1:
                            where = "FID_bikepathB = " + str(x) + " AND FID_scenic_pathsB = " + str(y) + " AND FID_trailsB = " + str(z)
                            print where
                            arcpy.Select_analysis(output + "LineUnion", output + "LineUnionSel", where)
                            arcpy.Dissolve_management(output + "GOODLAND", output + "GOODLAND_D", "", "", "MULTI_PART", "DISSOLVE_LINES")
                            arcpy.Clip_analysis(output + "GOODLAND_D", output + "PTS_B", output + "GOOD", "")
                            arcpy.Clip_analysis(output + "GOOD", output + "LineUnionSel", output + "NEWGOOD", "")
                            arcpy.Clip_analysis(output + "habitatvalue", output + "NEWGOOD", output + "habitatvalueC", "")
                            arcpy.Clip_analysis("floodzones", output + "habitatvalueC", res + "H" + str(s) + "P" + str(b) + "L" + str(l) + "_" + str(n), "")
                            n = n + 1
                        
                      
## Tools from the model are below 

###arcpy.Select_analysis(habitatsuit, habitatvalue, "grid_code = 7") 
###arcpy.Merge_management("LAND6;LAND3", GOODLAND, "")                      
###arcpy.Dissolve_management(GOODLAND, GOODLAND_D, "", "", "MULTI_PART", "DISSOLVE_LINES")
###arcpy.Merge_management("pointsB;pointsD", GOODPTS, "")
###arcpy.Buffer_analysis(GOODPTS, PTS_B, "1250 Meters", "FULL", "ROUND", "ALL", "", "PLANAR")
###arcpy.Clip_analysis(GOODLAND_D, PTS_B, GOOD, "")
###arcpy.Buffer_analysis(bikepaths, bikepathsB, "500 Meters", "FULL", "ROUND", "ALL", "", "PLANAR")
###arcpy.Buffer_analysis(trails, trailsB, "500 Meters", "FULL", "ROUND", "ALL", "", "PLANAR")
###arcpy.Buffer_analysis(scenic_paths, scenic_pathsB, "500 Meters", "FULL", "ROUND", "ALL", "", "PLANAR")
###arcpy.Union_analysis("D:\\Dropbox\\pgis_fall2017\\Assignment5\\partB.gdb\\bikepathsB #;D:\\Dropbox\\pgis_fall2017\\Assignment5\\partB.gdb\\trailsB #;D:\\Dropbox\\pgis_fall2017\\Assignment5\\partB.gdb\\scenic_pathsB #", LineUnion, "ALL", "", "GAPS")
###arcpy.Select_analysis(LineUnion, LineUnionSel, "FID_bikepathsB = 1 AND FID_scenic_pathsB = 1 AND FID_trailsB = -1")
###arcpy.Clip_analysis(GOOD, LineUnionSel, NEWGOOD, "")
###arcpy.Clip_analysis(habitatvalue, NEWGOOD, habitatvalueC, "")
##arcpy.Clip_analysis(floodzones, habitatvalueC, final, "")
