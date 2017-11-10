import arcpy

w=arcpy.env.workspce='C:/gispy/data/ch06'

arcpy.Frequency_analysis('park.dbf', 'COVER_freq.dbf', frequency_fields='COVER')