import arcpy, os

w=arcpy.env.workspace = "C:/gispy/sample_scripts/ch07/"
arcpy.env.overwriteOutput = 1

firstFile = arcpy.GetParameterAsText(0)

secondFile = arcpy.GetParameterAsText(1)

baseName = os.path.basename(firstFile)

extensionName = os.path.splitext(firstFile)[1]

filePathName = os.path.dirname(secondFile)

size = os.path.getsize(secondFile)

#scriptPath = os.path.abspath(__file__)
#scriptDir = os.path.dirname(scriptPath)

print baseName

print extensionName

#if filePathName == "":
#    print "No file path available"
#else
#        print filePathName

print size

print os.listdir(scriptDir)
