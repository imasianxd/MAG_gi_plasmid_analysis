#usr/bin/bash

#prior to this, plasmid_perbase.tsv was cleaned up in excel: for plasmids recovered in more than 1 bin, select the bin with the highest % per-base recovery of the plasmid (remove the other duplicates)
#this creates a new file: plasmid_perbase_clean.tsv

#add header
echo $'species\tbiosample_acc\trefseq_acc\ttype\tbin\tplasmidlen\tmatchlen\tpercent_rec' > summary_plasmidrecovery.tsv

#include the un-recovered plasmid
join -t $'\t' -1 3 -2 2 -a1 -e "NA" -o '1.1,1.2,1.3,1.4,2.1,1.5,2.4,2.5' \ #join
<(sort -k3 -t $'\t' taxa_metadata_plasmid.tsv) \ #metadata file including ALL reference plasmids
<(awk -v "OFS=\t" '{$2=$2;sub(/\.1/,"",$2); print}' plasmid_perbase_clean.tsv |tail -n +2 | sort -k2 -t $'\t') |\ # recovered plasmids + %recovery
awk -F'\t' '{ $7 = ($7 == "NA" ? 0 : $7) } 1' OFS='\t'|\ #change match length to zero if NA
awk -F'\t' '{ $8 = ($8 == "NA" ? 0 : $8) } 1' OFS='\t' \ #change per base recovery to zero if NA
>> summary_plasmidrecovery.tsv
