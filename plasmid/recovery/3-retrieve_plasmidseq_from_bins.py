#usr/bin/python

DIR='/Users/Venusl/Desktop/MAG'
DIRseq=DIR+'/_bins'
DIRblast=DIR+'/plasmid/recovery/blastout50'

import os
import re

os.system('mkdir -p '+DIR+'/plasmid/recovery/seq_by_plasmid')

for b in os.listdir(DIRblast): #iterate through the bins
    for f in os.listdir(DIRblast+'/'+b): #iterate through each file within the bins
        fn=(f.split('.'))[0]
        
        os.system('mkdir -p '+DIR+'/plasmid/recovery/seq_by_plasmid/'+b)
        #make a temporary bed file for bedtools
        os.system('cut -f2,11,12 '+DIRblast+'/'+b+'/'+f+' > '+DIRblast+'/'+b+'/tmp_'+fn+'.bed') #create a tmp .bed file
        
        #re-order coordinates if start position is greater than end position
        outbed= open(DIRblast+'/'+b+'/tmpnew_'+fn+'.bed', 'w')
        with open(DIRblast+'/'+b+'/tmp_'+fn+'.bed', 'r') as blastfile:
            for line in blastfile:
                l= line.split()
                contig=l[0]
                start=l[1]
                end=l[2]
                
                startnew=0
                endnew=0

                if int(start) < int(end):
                    startnew=start
                    endnew=end
                else:
                    startnew=end
                    endnew=start
                outbed.write(contig+'\t'+startnew+'\t'+endnew+'\n')
        outbed.close()
        
        #retrieve sequences
        fi=DIRseq+'/'+b+'.fa'
        bed=DIRblast+'/'+b+'/tmpnew_'+fn+'.bed' #file with format: genome_name, start_coordinate, end_coordinate
        fo=DIR+'/plasmid/recovery/seq_by_plasmid/'+b+'/tmp_'+fn+'_plasmid.fa'

        cmd='bedtools getfasta -fi '+fi+' -bed '+bed+' -fo '+fo
        os.system(cmd)
        os.system('rm '+DIRblast+'/'+b+'/tmp*') #remove tmp .bed files
        
        #format fasta headers...from... >ID:START-STOP to...  >ID|START|STOP
        newseqfile=open(DIR+'/plasmid/recovery/seq_by_plasmid/'+b+'/'+fn+'_plasmid.fa','w')
        with open(fo, 'r') as o:
            for line in o:
                if '>' in line:
                    line_sp=line.split(':')
                    line_a=line_sp[0]
                    line_b=line_sp[1]
                    line_b=re.sub('-','|',line_b)
                    line=line_a+'|'+line_b
                    
                    newseqfile.write(line)
                else:
                    newseqfile.write(line)
        o.close()
        
        os.system('rm '+fo)
