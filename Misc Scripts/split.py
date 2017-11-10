import arcpy

w=arcpy.env.workspace = 'C:/gispy/data/ch06'

arcpy.Split_analysis('park.shp', 'workzones.shp', 'Zone', 'C:/gispy/scratch/zones.shp')