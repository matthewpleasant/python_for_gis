import arcpy

w=arcpy.env.workspace = arcpy.GetParameterAsText(0)

shapefile = arcpy.GetParameterAsText(1)

KMLoutput = arcpy.GetParameterAsText(2)

scale = arcpy.GetParameterAsText(3)

arcpy.MakeFeatureLayer_management(

arcpy.LayerToKML_conversion(