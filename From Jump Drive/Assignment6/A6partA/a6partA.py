d = {}
input = file('C:/Users/matthewpleasant/Desktop/A6partA/indata.txt', "r")
output = file('C:/Users/matthewpleasant/Desktop/A6partA/outdata.txt', "w")

for l in input:
        info = l.split(",")
        info[2] = info[2].replace("\n", "")
        if info[0] in d.keys():
                value = d[info[0]]
                if int(value[1]) > int(info[2]) and info[2] != "0":
                        value[1] = info[2]
                if info[1] == '"YES"':
                        value[0] = info[1]
                d[info[0]] = value
        elif info[0] not in d.keys() and info[2] != "0":
                key = info[0]
                d[key] = [info[1], info[2]]

for i in d.items():
        output.write(i[0] + "," + i[1][0] + "," + i[1][1] + "\n")

output.close()