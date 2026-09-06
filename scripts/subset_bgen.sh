#!/bin/bash

# Subset BGEN file and convert to VCF using qctool
# Usage: ./subset_bgen.sh input.bgen input.sample subset.sample output_prefix

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <input.bgen> <input.sample> <subset.sample> <output_prefix>"
    exit 1
fi

INPUT_BGEN=$1
INPUT_SAMPLE=$2
SUBSET_SAMPLE=$3
OUTPUT_PREFIX=$4

echo "Subsetting BGEN and converting to VCF..."
#echo "qctool -g ${INPUT_BGEN} \
#       -s ${INPUT_SAMPLE} \
#       -incl-samples ${SUBSET_SAMPLE} \
#       -ofiletype vcf \
#       -og ${OUTPUT_PREFIX}.vcf"


/usr/local/bin/qctool -g ${INPUT_BGEN} \
       -s ${INPUT_SAMPLE} \
       -incl-samples ${SUBSET_SAMPLE} \
       -ofiletype vcf \
       -og ${OUTPUT_PREFIX}.vcf

echo "Done! Output file: ${OUTPUT_PREFIX}.vcf"
