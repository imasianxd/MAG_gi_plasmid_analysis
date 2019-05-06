#!/bin/bash -l

#SBATCH --workdir=/scratch/vlauu
#SBATCH --account=rrg-fiona-ad
#SBATCH --job-name=mag_plasmid_blast
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=18
#SBATCH --mem-per-cpu=3500M
#SBATCH --time=11:50:00
#SBATCH --mail-user=<venusl@sfu.ca>
#SBATCH --mail-type=ALL

module load nixpkgs/16.09
module load gcc/7.3.0
module load blast+/2.7.1

#run blastn on reference plasmids against contigs in bins

OIFS="$IFS"
IFS=$'\n'

DIR='/home/vlauu/project/shared/MAGAssessment'

for i in `ls $DIR/sequences`;
do
    #$i is the spp name
    echo "$i";
    for k in `ls "$DIR"/sequences/"$i"/*/`;
    do 
	echo "$k"; #this is either chr or plasmid
	if [ "$k" == 'plasmid' ]
	then
	    for j in `ls "$DIR"/sequences/"$i"/*/"$k"/*.fasta`;
		     #$j is the fasta name
	    do
		echo $j;
		filename=$(basename "$j" .fasta);

		for l in `ls "$DIR"/plasmid/blastdb`;
		do
		    echo dbname: "$l";
		    mkdir -p "$DIR"/plasmid/blastout/"$l";
		    blastn -db "$DIR"/plasmid/blastdb/"$l"/"$l" -query "$j" -outfmt "6 qseqid sseqid pident nident qlen slen length qstart qend mismatch gapope evalue bitscore" -out "$DIR"/plasmid/blastout/"$l"/"$filename".tab;
		done;
	    done;
	fi
    done;
done;

IFS="$OIFS"
