import arcpy

## Example:
## Explain the following statement.
# The following statement sets the overwriteOutput parameter of the env class
# to automtically overwrite output
arcpy.env.overwriteOutput = True

## Note - next two statements below should reflect where your data is (no explanation!)
arcpy.env.workspace = "C:/Users/mpleasan/Desktop/a4/infolder/"
out = "C:/Users/mpleasan/Desktop/a4/outfolder/out.gdb/outdata/"

## Explain the following statements.
# The following statement retrieves a list of file geodatabase workspaces
#and stores it in the variable wslist. The next statement does the same for
# variable fldlist, but only for shapefile workspace
wslist = arcpy.ListWorkspaces('',"FileGDB")
fldlist = arcpy.ListWorkspaces('',"Folder")

## Explain the code below.
# This code uses a condition to determine if the wslist is empty.
# If it's empty, it prints "No geodatabases" because the code above found no geodatabases.
# Otherwise, the code loops through the list stored in wslist, printing each.
# The remaining lines (from fldlist down) do the same, except for the second list
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
# The following assignment statement creates a new list by
# concatenating the lists stored in wslist and fldlist
allws = wslist+fldlist

## Explain the following statement.
# This assigns an empty list to the allfcs variable
allfcs =[]

## Explain the following section of code and what the final output
## of this section of code is
# This loops through all the workspaces. It sets the environment
# to the workspace stored in the interative variable "a." Then it
# creates a list of feature classes stored in the current environment
# A nested for loop iterates through the list of feature classes,
# concatenating the name of the file with the workspace. It then stores them
# in the list "allfcs." The latter half of the code does the same operation,
# but this time it checks for datasets in current environment, creates a list
# of features stored in those, concatenates the name to create a full filepath
# and then adds the new items to "allfcs." The end product is a list
# containing all the feature classes in "infolder."

for a in allws: 
    arcpy.env.workspace = a 
    fcs = arcpy.ListFeatureClasses() 
    i = 0 
    for f in fcs: 
        fcs[i] = a+"\\"+ f 
        i = i+1 
    allfcs = allfcs + fcs
    dslist = arcpy.ListDatasets() 
    if dslist == []: 
        continue 
    else: 
        for d in dslist:
            fdfc = arcpy.ListFeatureClasses("","",d) 
            i = 0
            for f in fdfc: 
                fdfc[i] = a + "\\" + d + "\\" + f 
                i=i+1
            allfcs = allfcs + fdfc

## Explain the following section of code and what the final output
## of this section of code is

# This loop creates a describe object for each feature in allfcs and prints the
# shape file type. It checks the shape type property in each describe object and
# sets a variable with a buffer value of 200, 300 or 500 depending on the type. The
# script then turns the buffer value into a string, concatenates it with the string " Meters"
# and stores it in the variable "bdis." 
# It then uses the buffer analysis tool to buffer each file using this variable. The output
# receives the name "BUF" and a number stored in the variable "n," which increases with each iteration
# The code then creates an empty listi, "fldnames," and stores the field objects of the current file.
# It checks if one of the fields is named "Checked," and if there isn't one, it adds one. The new field
# is a text field with a character length of three.
# The output of the script below are buffered versions of all the feature classes with distances depending
# on their shape type. All the input files used will now have a field named "Checked."

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
