import arcpy

## Example:
## Explain the following statement.
# The following statement sets the overwriteOutput parameter of the env class
# to automtically overwrite outputs 
arcpy.env.overwriteOutput = True

## Note - next two statements below should reflect where your data is (no explanation!)
#arcpy.env.workspace = "C:\\Users\\sreader\\Dropbox\\pgis_fall2017\\class3i\\c5\\infolder"
arcpy.env.workspace = "C:/Users/mpleasan/Desktop/a4/infolder/" 
#out = "C:/Users/mpleasan/Desktop/a4/outfolder/out.gdb/outdata/"

## Explain the following statements.
# The following statememt retrieves a list of file geodatabase workspaces and stores it
# in the variable wslist. The next satement the same, but only for folders
wslist = arcpy.ListWorkspaces('',"FileGDB")
fldlist = arcpy.ListWorkspaces('',"Folder")

## Explain the code below.
# The following code uses a condition to determine if the wslist is empty.
# If it's empty, it prints "No geodatabases" because the code above found none
# Otherwise, the code loops through the list stored in wslist, printing each.
# The remaining lines (from fldlist on down) do the same, except for the second list
# created above and stored in "fldlist"
if wslist == []:
    print 'No Geodatabases'
else:
    print "Geodatabases:"
    for ws in wslist:
        print ws
if fldlist == []:
    print 'No Shapefile Folders'
else:
    print "Shapefile Folders:"
    for f in fldlist:
        print f

## Explain the following statement.
# The following assignment statement concatenates the wslist and fldlist together, creating one list -- right?
allws = wslist+fldlist

## Explain the following statement.
# This assigns an empty list to the allfcs variable
allfcs =[]

## Explain the following section of code and what the final output
## of this section of code is

for a in allws: # This sets up a loop that iterates through the list of workspaces stored in the allws variable
    arcpy.env.workspace = a # Sets the current workspace to the workspace assigned in "a," the current item in the loop
    fcs = arcpy.ListFeatureClasses() # Stores a list of the feature classes in the current workspace to the variable fcs
    i = 0 # Initalizes a count variable, starting at 0
    for f in fcs: # Nests a loop that iterates through the list of feature classes stores in fcs
        fcs[i] = a+"\\"+ f # Assigns a string with the workspace and feature class name to index 0 for the fcs list 
        i = i+1 # Adds 1 to the count variable
    allfcs = allfcs + fcs # Adds allfcs and fcs, creating a single list
    dslist = arcpy.ListDatasets() # Lists the datasets in the current workspace (assigned above)
    if dslist == []: 
        continue # Bypasses this code if list is empty
    else: # if dslist isn't empty, it will perform the following operations:
        for d in dslist:
            fdfc = arcpy.ListFeatureClasses("","",d) # stores a list of features classes in the current dataset stored as a list in dslist
            i = 0 # initializes a count variable
            for f in fdfc: # for each feature class store in fdfc, will perform the following operations:
                fdfc[i] = a + "\\" + d + "\\" + f # reassigns the current it of the list with the full pathfile
                i=i+1 # adds 1 to the count
            allfcs = allfcs + fdfc # concatenates the lists together

## Explain the following section of code and what the final output
## of this section of code is

# This loop creates a describe object for each feature set and prints the
# shape file type. Depending on the shape file type, it sets a variable with
# the a buffer value of 200, 300 or 500. It then uses the buffer analysis tool
# to buffer each file using the value set previously in the script. It then adds
# a field name to each ----- ? 

n=1
for f in allfcs: 
    desc = arcpy.Describe(f)
    print desc.shapeType
    if desc.shapeType == "Polygon": bufd = 200
    elif desc.shapeType == "Polyline": bufd = 300
    elif desc.shapeType == "Multipoint": bufd = 500
    bdis = str(bufd) + " Meters"
    arcpy.Buffer_analysis(f, out+"BUF"+str(n), bdis, "FULL", "ROUND", "ALL", "")
    fldnames=[]
    for z in desc.Fields:
        fldnames.append(z.Name)
    if not "Checked" in fldnames:
        arcpy.AddField_management(f,"Checked","TEXT", "#","#",3)
    n=n+1
