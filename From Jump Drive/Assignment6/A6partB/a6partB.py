import arcpy

# arcpy.Intersect_analysis(in_features="trails #;floodplain #", out_feature_class="C:/Users/mpleasan/Documents/ArcGIS/Default.gdb/intersect_attempt", join_attributes="ALL", cluster_tolerance="-1 Unknown", output_type="POINT")

ws = arcpy.env.workspace = "C:/Users/matthewpleasant/Desktop/A6partB/"

sc = arcpy.da.SearchCursor("intersect.shp", ["Shape@"])

point = []
newlist = []

wearr = arcpy.Array()
snarr = arcpy.Array()
ewarr = arcpy.Array()
nsarr = arcpy.Array()

arcpy.CreateFeatureclass_management(ws, "new_lines.shp", "POLYLINE", "#", "DISABLED", "DISABLED",  ws + "intersect.prj")

for r in sc:
    for q in r[0]:
        x = [q.X, q.Y]
        if x not in point:
            point.append([q.X, q.Y])


##### WEST TO EAST LINE ####

point.sort()

for i in point:
    wearr.add(arcpy.Point(float(i[0]),float(i[1])))

ic = arcpy.da.InsertCursor("new_lines.shp", "Shape@")

ic.insertRow([arcpy.Polyline(wearr)])

##### SOUTH TO NORTH LINE ####

sn = sorted(point, key=lambda points: points[1])

for i in sn:
    snarr.add(arcpy.Point(float(i[0]),float(i[1])))

ic = arcpy.da.InsertCursor("new_lines.shp", "Shape@")

ic.insertRow([arcpy.Polyline(snarr)])

#### EAST TO WEST LINE ####

point.reverse()

for i in point:
    ewarr.add(arcpy.Point(float(i[0]),float(i[1])))

ic.insertRow([arcpy.Polyline(ewarr)])

#### NORTH TO SOUTH LINE ####

sn.reverse()

for i in sn:
    nsarr.add(arcpy.Point(float(i[0]),float(i[1])))

ic.insertRow([arcpy.Polyline(nsarr)])

del sc
del ic