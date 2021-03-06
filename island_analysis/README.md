#MAG Genomic Island Analysis

Instructions for replicating the genomic island component of the MAG analysis

## Input Files

- MAG Bin Files:
    - FASTA formatted contigs (single file per bin with all contigs)
    - GenBank formatted contigs with annotations (single file per bin with all contigs)
- Reference genomes table (currently called chrRef.tsv)

## Pre-processing

- **Size Filtering**
    - Script: size_filter.py
    - Usage: size_filter.py -i INPUT -o OUTPUT -s SIZE -f FORMAT
    - Notes: Removing contigs < 1 kb is recommended for using IslandViewer. Note that both the GenBank files submitted to 
IslandViewer and the FASTA formatted files used later in the analysis should be filtered.

## Running IslandViewer

- **Submitting Draft Genomes**
    - Script: submit_bins_as_draft.py
    - Usage: submit_bins_as_draft.py -r REF_GENOMES -a AUTH_TOKEN -e EMAIL -g GENOME_DIR -l LOG
    - Warning: If the directory structure for storing the annotated GenBank files changes from how the original MAG bin 
    files were stored then you'll probably need to make some small edits to this file
    - Notes: The log file will later be used to retrieve the results - it contains the submitted job info

- **Downloading IslandViewer Results**
    - Script: download_IV_results.py
    - Usage: download_IV_results.py -j JOBIDS_LOG -a AUTH_TOKEN \[-o OUTDIR\]
    - Notes: Downloads the genbank and csv (genes) formatted results

- **Reformatting IslandViewer Results**
    - Script: IV_Results_Reformatting.py
    - Usage: IV_Results_Reformatting.py -i ISLANDVIEWER_INPUT -o OUTPUT
    - Notes: Processes the csv file containing GI genes. Produces a tsv file with the GI coordinates.

## Analysing IslandViewer Results

- **Preparing a BLAST Database for Concatenated Genomes**
    - Script: FASTA_database_Maker.py
    - Usage: FASTA_database_Maker.py -g GENOME_DIRECTORY -d DATABASE_FASTA
    - Warning: After creating the fasta file, you **still need to run makeblastdb to generate the BLAST database**.
    Command for this: makeblastdb -in <FASTA_FORMATTED_GENOMES_DATABASE> -dbtype nucl -parse_seqids -out <OUTFILE_PREFIX>
    - Notes: This script kinda assumes all your concatenated genomes results files downloaded from IslandViewer are 
    stored in the same directory. This could probably be handled better, but that's how I was storing things anyways...

- **Contig Mapping**
    - Script: contig_mapper.py
    - Usage:  contig_mapper.py -f FASTA -b BLAST_OUT -d BLAST_DB -g GENOME_NAME -o OUTPUT_MAP
    - Notes: Takes the FASTA version of the contigs and BLASTs them against the concatenated genomes in order to 
    determine the coordinates of each contig in the corresponding concatenated genome generated by IslandViewer

- **Genomic Island Contig Splitting**
    - Script: split_GI_chrom.py
    - Usage: split_GI_chrom.py -i INPUT_FASTA -v IV_GIS -n NAME -o OUTDIR -a ALIGNMENT_FILE
    - Notes: Uses the genomic island coordinates and mapping of the contigs to the concatenated genome to split the 
    sequences into chromosome and GI files