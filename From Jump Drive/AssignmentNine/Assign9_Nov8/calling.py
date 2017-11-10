import arcpy, assign9p2
reload(assign9p2)

arcpy.env.overwriteOutput = "True"

wksp=arcpy.env.workpace = "C:/Users/mpleasan/Desktop/Assign9_Nov7/c11ex2.gdb/manatee/"
inf = "C:/Users/mpleasan/Desktop/c11ex2/coords.txt"
sep = ";"
bd = [100,200,300]
ibd = [250,500]

out = assign9p2.coords(inf, sep, bd)
assign9p2.buff(ibd, out)