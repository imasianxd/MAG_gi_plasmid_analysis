#usr/bin/bash

DIR='/home/vlauu/project/shared/MAGAssessment/plasmid/recovery'

mkdir -p $DIR/seq

for b in `ls $DIR/seq_by_plasmid`;
do  
   #b is the bin number (subdirectory)
   bins="${b//./_}"
   echo "$bins"
   cat $DIR/seq_by_plasmid/$b/* > $DIR/seq/${bins}_plasmid.fasta;
done;

