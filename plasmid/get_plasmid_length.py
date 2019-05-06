#usr/bin/python3

#count length of refseq plasmids

import subprocess

DIR='/home/vlauu/project/shared/MAGAssessment'


OUT=open(DIR+"/plasmid/taxa_metadata_plasmid.tsv", "w")
with open(DIR+"/taxa_metadata.tsv","r") as f:
    for line in f:
        line.rstrip()
        
        sp,biosam_acc,refseq_acc,genometype =line.split("\t")
        
        if 'plasmid' in line:
            cmd="grep '\ssource' "+ DIR+"/completeGenbanks/"+refseq_acc+"*.gb"
            grepout=(subprocess.check_output([cmd], shell=True)).decode("utf-8")

            coord=grepout.split()[1]
            print(refseq_acc+' coord: '+coord)
            end= coord.split('..')[1] #length of plasmid
            print('end: '+end)
            OUT.write(sp+"\t"+biosam_acc+"\t"+refseq_acc+"\tplasmid\t"+end+'\n')

OUT.close()
