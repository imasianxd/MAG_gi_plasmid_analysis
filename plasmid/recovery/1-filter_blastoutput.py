#!usr/bin/python3

#Select blast hits in which over 50% of the contig length is matched to a plasmid  

DIR='/home/vlauu/project/shared/MAGAssessment/plasmid'

import os

for b in os.listdir(DIR+'/blastout'): #iterate through bins
    if not os.path.isdir(DIR+'/recovery/blastout80/'+b):
        os.mkdir(DIR+'/recovery/blastout80/'+b)
    print(b)
    for f in os.listdir(DIR+'/blastout/'+b): #iterate through each file within the bins
        OUT=open(DIR+"/recovery/blastout80/"+b+'/'+f, "w")
        with open(DIR+"/blastout/"+b+'/'+f,"r") as k:

            for line in k:
                line.rstrip()
                splitline=line.split()
                slen=int(splitline[4])
                length=int(splitline[5])
                percent=length/slen*100
                
                if percent > 50:
                    print(line)
                    OUT.write(line)
        OUT.close()
