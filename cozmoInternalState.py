# import pandas as pd
lines = None
with open('functions_cozmo.txt', 'r') as file:
    lines = file.readlines()
print(lines, "\n")

with open("functions_cozmo.txt",'w') as file:
    for i,line in enumerate(lines,1):         ## STARTS THE NUMBERING FROM 1 (by default it begins with 0)    
        if '-' in line:                              ## OVERWRITES line:2
            file.writelines("")
        else:
            file.writelines(line)
