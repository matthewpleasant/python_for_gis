d = {}
input = file('indata.txt', "r")
for line in input.readlines():
    values = line.split(",")
    fn = values[0]
    S = values[1]
    J = values[2]
    J = int(J)
    if fn not in d:
        d[fn] = [S,J]
    else:
        if not J == 0:
            if d[fn][1] == 0:
                 d[fn][1] = J
            if J < d[fn][1]:
                 d[fn][1] = J
        if S == '"YES"':
            d[fn][0] = S
input.close()
of = open("out5.txt", 'w')
a = d.keys()
for x in a:
    of.write(x + "," + d[x][0] + "," + str(d[x][1])+'\n')
of.close()   

    



    
    
    
    

    
    