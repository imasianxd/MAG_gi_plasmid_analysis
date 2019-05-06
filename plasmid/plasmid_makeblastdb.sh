#!/bin/bash -l
#
#SBATCH --workdir=/scratch/vlauu
#SBATCH --account=rrg-fiona-ad
#SBATCH --job-name=mag_plasmid_blast
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=18
#SBATCH --mem-per-cpu=3500M
#SBATCH --time=23:50:00
#SBATCH --mail-user=<venusl@sfu.ca>
#SBATCH --mail-type=ALL

module load nixpkgs/16.09
module load gcc/7.3.0
module load blast+/2.7.1

#make a local blast database using all contig bins

OIFS="$IFS"
IFS=$'\n'

DIR='/home/vlauu/project/shared/MAGAssessment'

for i in `ls "$DIR/_bins"`;
do
    #$i is the bin name
    echo "$i";
    name=$(basename $i .fa);
    mkdir "$DIR/plasmid/blastdb/$name"
    makeblastdb -in "$DIR/_bins/$i" -dbtype nucl -parse_seqids -out "$DIR/plasmid/blastdb/$name/$name";
done;

IFS="$OIFS"
