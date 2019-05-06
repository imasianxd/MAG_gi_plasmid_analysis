#usr/bin/python

#use python3

#calculate per-base recovery of plasmids within each bin, based on contigs with >50% of length matching to reference plasmids


DIR='/home/vlauu/project/shared/MAGAssessment/plasmid/recovery'

import os

#function for calculating overlaps between intervals (genome coordinates between contigs within a bin)
def getOverlap(a, b):
    return max(0, min(a[1], b[1]) - max(a[0], b[0]))+1


OUT=open(DIR+"/plasmid_perbase.tsv", "w")
OUT.write('bin\taccession\tplasmdlen\tmatchlen\tpercent_rec\n')

for b in os.listdir(DIR+'/blastout50'): #iterate through bins
    #print(b)
    for f in os.listdir(DIR+'/blastout50/'+b): #iterate through each file within the bins
        os.system('sort -k9 -n '+DIR+'/blastout50/'+b+'/'+f+' > '+DIR+'/blastout50/'+b+'/tmp_'+f) #create a tmp blast output file sorted by the start coordinate of refseq plasmid
        qseqid=0
        matchlen=0
        plen=0

        start1=0
        end1=0
        start2=0
        end2=0

        print('CURRENT FILE: '+f)
        with open(DIR+"/blastout50/"+b+'/'+f,"r") as k:
            for line in k:
                splitline=line.split()
                qseqid=splitline[0]
                plen=int(splitline[3])
                mlen=int(splitline[5])
                start2=int(splitline[8])
                end2=int(splitline[9])

                overlap=getOverlap([start1,end1], [start2,end2]) #detect overlaps between current contig and previous contig (previous line)
                
                if overlap > 0:
                    matchlen=matchlen+mlen-overlap
                else:
                    matchlen=matchlen+mlen
                    
                start1=start2
                end1=end2
                

                #matchlen=int(matchlen)+int(mlen)
        percent_rec = (matchlen/plen)*100 #percent of recovery of each plasmid, based on number of matched bases
        
        print(b+"\t"+qseqid+"\t"+str(plen)+"\t"+str(matchlen)+"\t"+str(percent_rec))
        OUT.write(b+"\t"+qseqid+"\t"+str(plen)+"\t"+str(matchlen)+"\t"+str(percent_rec)+'\n')
        os.system('rm '+DIR+'/blastout50/'+b+'/tmp_'+f)
OUT.close()

os.system('sort -V '+DIR+"/plasmid_perbase.tsv > "+DIR+"/plasmid_perbaseNEW.tsv")
os.system('mv '+DIR+"/plasmid_perbaseNEW.tsv "+DIR+"/plasmid_perbase.tsv")
