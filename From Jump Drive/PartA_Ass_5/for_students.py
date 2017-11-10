import arcpy, random

gooddata = "C:/Users/mpleasan/Desktop/PartA/analysis_inputs.gdb/indata/"
rootD = "C:/Users/mpleasan/Desktop/PartA/vendor.gdb"
res = "C:/Users/mpleasan/Desktop/PartA/results.gdb/"

arcpy.env.workspace = gooddata
fcs = arcpy.ListFeatureClasses()
if fcs:
    for f in fcs:
        arcpy.Delete_management(f)

v = "Verified"
proj = "NAD_1983_HARN_Albers"

for root, dirs, files in arcpy.da.Walk(rootD,datatype='FeatureClass'):
    arcpy.env.workspace = root
    for i in files:
        d = arcpy.Describe(i)
        if d.shapeType == "Polygon" or d.shapetype == "Polyline":
            for c in d.Fields:
                if c.name == v and c.length == 3 and d.spatialReference.name == proj: 
                    arcpy.CopyFeatures_management(i, gooddata +  "my" + i)
        elif d.shapeType == "Point":
            cnt = arcpy.GetCount_management(i)
            cnt = int(cnt.getOutput(0))
            if cnt == 1:
                arcpy.CopyFeatures_management(i, gooddata + "my" + i)

arcpy.env.workspace = res
fcs = arcpy.ListFeatureClasses()
if fcs:
    for f in fcs:
        arcpy.Delete_management(f)

arcpy.env.overwriteOutput = True
arcpy.env.workspace=gooddata

ptfcs = arcpy.ListFeatureClasses('',"Point")
stnbuf = [2.5,3.0,3.5]
rdsbuf = [1.0,1.5,2.0]
strmbuf = [0.5,1.0,1.5]
npts = [50,75,100]

nruns = 3 ##Sets the number of runs to 1 
for i in range (1,nruns): ##Creates list that's only 1
    nstat = random.randint(4,8) ## Picks a random integer between 4 and 8
    print "nstat equals: " + str(nstat)
    xx = random.sample(ptfcs,nstat) ## Picks the number of files set above from the feature classes listed in ptfcs, stores the list xx
    arcpy.Merge_management(xx, "stations_Merge") ## merges the files together, output is called "stations_Merge"
    rbuf = random.choice(rdsbuf) ## randomly chooses an element from the rdsbuf list
    sbuf = random.choice(strmbuf) ## randomly chooses an element from the strmbuf list
    for n in npts: ## Performs the following loop for each value in the npts list -- 50, 75, 100
        rpts = str(n) ## Creates string of npts list item -- '50', '75', or '100'
        for s in stnbuf: ## Performs the following loop for each item in the stnbuf list -- 2.5, 3.0, 3.5
            buf1= str(s) + " Kilometers" ## Creates string out of the items in stnbuf -- '2.5 Kilometers', '3.0 Kilometers', '3.5 Kilometers'    
            arcpy.Buffer_analysis("stations_Merge", "stationsBuf", buf1, "FULL", "ROUND", "ALL", "", "PLANAR") ## Buffers each station based on distance set in buf1

            ## STREAMS
            # For the buffer tool below, create the necessary value for sbuffer      
            sbuffer = str(sbuf) + " Kilometers" 
            arcpy.Buffer_analysis("mystreams", "mystreams_Buffer", sbuffer, "FULL", "ROUND", "ALL", "", "PLANAR")
            arcpy.Erase_analysis("stationsBuf", "mystreams_Buffer", "stationsErase1", "")

            ## ROADS
            # For the buffer tool below, create the necessary value for rbuffer     
            rbuffer = str(rbuf) + " Kilometers"
            arcpy.Buffer_analysis("myroads", "myroads_Buffer", rbuffer, "FULL", "ROUND", "ALL", "", "PLANAR")
            arcpy.Erase_analysis("stationsErase1", "myroads_Buffer", "stationsErase", "") 
            arcpy.Clip_analysis("mysoildrain", "stationsErase", "mysoildrainClip", "")
            arcpy.Dissolve_management("mysoildrainClip", "mysoildrainDiss", "DRAINAGECL", "", "MULTI_PART", "DISSOLVE_LINES") ## DISSOLVE "mysoildrainDiss"
            arcpy.Clip_analysis("myhabsuit", "stationsErase", "myhabsuitClip", "")
            arcpy.Dissolve_management("myhabsuitClip", "myhabsuitDiss", "Suitability", "", "MULTI_PART", "DISSOLVE_LINES") ## DISSOLVE "myhabsuitDiss"
            arcpy.Clip_analysis("mybasins", "stationsErase", "mybasinsClip", "")
            arcpy.Dissolve_management("mybasinsClip", "mybasinsDiss", "BASIN", "", "MULTI_PART", "DISSOLVE_LINES") ## DISSOLVE "mybasinsDiss"

            # Create a value table object with 2 columns and populate it with the names of the feature classes that will be union'ed and
            # the '#' for the priority ranks
            vt1 = arcpy.ValueTable(2) ## MY CODE
            vt1.addRow("mysoildrainDiss" + " #") 
            vt1.addRow("myhabsuitDiss" + " #") 
            vt1.addRow("mybasinsDiss" + " #") 
            arcpy.Union_analysis(vt1, "sampling_space", "NO_FID", "", "GAPS")
            arcpy.CreateRandomPoints_management(gooddata, "x1", "", "sampling_space", rpts, "100 Meters", "POINT", "0")

            # You now need to generate a string that will be used for the final feature class names
            # However, since all the buffer distances are floats (have a decimal point) you need to first create string versions of these
            # distances without the decimal point - remember the decimal point is not valid in a feature class name.
            # Think about a string method that will help with this.
            rbufout = str(rbuf).replace(".","") 
            sbufout = str(sbuf).replace(".","") 
            stnbufout = str(s).replace(".","") 

            # Then using these 3 string variables and others defined in the script, create a string which will be the feature class output name - see page 3 of problem statement
            # for an example. General note re developing strings that are long and depend on variables: develop and test your string in the 'interactive window environment'
            # BUT make sure all variables needed by the string have been defined. Since we probably don't want to run the script here just yet, you can just assign example values
            # for the variables in the interactive window  before using them in creating the string
            ostring =  "Stns_" + str(nstat) + "_" + stnbufout + "_Rds_" + rbufout + "_Strm_" + sbufout 
           
            # There is a possibility that we may generate the same scenario (ie the same feature class name) more than once (when the number of runs is more than 1)
            # and we don't want to overwrite an existing output.
            # So, how can we test to see if a feature class with the name you just defined above already exists, and, if it does, we need to add
            # an appropriate suffix to the name so that we keep both - however, note that this repetition could occur more than once, so the suffix
            # needs to be coded so all repetitions can be individually identified - since repetition won't occur inside a run, what might be a good value to use in a suffix?

            if arcpy.Exists(ostring): 
                ostring = ostring + "_" + str(i) 
              
            ## < your code for the above issue here> 

            arcpy.Intersect_analysis("x1 #; sampling_space #", res+ostring, "NO_FID", "", "POINT")
            
            # Since we will need access to the output from the next tool, assign its output to a variable (what type of object will this variable be?)
            resultObj = arcpy.GetCount_management(res+ostring) ## MY CODE
            # From the variable (object) you created by editing the above line, now retrieve, as an integer, the first output of that object
            c = resultObj.getOutput(0) ## MY CODE
            # Now create a string variable to produce the four lines of output as given by the example on page 3 of the problem statement
            pstring = "{0} Stations with Buffer {1}, {2} points, Road buffer of {3}, Stream Buffer of {4} is: {5}".format(nstat, rpts, s, rbuf, sbuf, c)
            print pstring

# Finally, now you have generated all your ouputs (thru looping), you need to merge all of them into one
# Write the code below that will do this - and produce a final feature class called "allpoints" in the results.gdb
## < your code for the above issue here>
arcpy.env.workspace=res
files = arcpy.ListFeatureClasses()
print files
vt2 = arcpy.ValueTable(1)
for f in files:
    vt2.addRow(f)
arcpy.Merge_management(files,"allpoints")
