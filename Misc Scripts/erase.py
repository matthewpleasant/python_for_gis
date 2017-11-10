import arcpy

w=arcpy.env.workspace = 'C:/gispy/data/ch06'

arcpy.env.overwriteOutput = True

arcpy.analysis.Erase(in_features='park.shp', erase_features='special_regions.shp', out_feature_class='C:/gispy/scratch/no_damage.shp')