#!/usr/bin/env python3

import sys
import gzip

def open_file(filename):
    """Open regular or gzipped file"""
    if filename.endswith('.gz'):
        return gzip.open(filename, 'rt')
    return open(filename, 'r')

def hard_call_haplotype(probs):
    """
    Hard-call haplotype based on max probability
    probs: list of 2 probabilities [p_ref, p_alt]
    Returns: 0 or 1
    """
    return 1 if probs[1] > probs[0] else 0

def parse_genotype(gt_field, gp_field):
    """
    Parse genotype field with GP probabilities
    gt_field: phased genotype string (e.g., "0|1" or ".|.") or None
    gp_field: GP probabilities string (e.g., "0,1,0,1") or None
    
    Returns: tuple of (hap1, hap2) as 0 or 1
    """
    # If we have GP probabilities, use them for hard-calling
    if gp_field is not None and gp_field != '.' and gp_field != '.,.,.,.':
        gp_values = [float(x) for x in gp_field.split(',')]
        # GP format: P(h1=ref), P(h1=alt), P(h2=ref), P(h2=alt)
        if len(gp_values) == 4:
            hap1 = hard_call_haplotype([gp_values[0], gp_values[1]])
            hap2 = hard_call_haplotype([gp_values[2], gp_values[3]])
            return hap1, hap2
    
    # Fallback to GT field if GP not available
    if gt_field is not None and '|' in gt_field:
        alleles = gt_field.split('|')
        hap1 = 0 if alleles[0] == '.' else int(alleles[0])
        hap2 = 0 if alleles[1] == '.' else int(alleles[1])
        return hap1, hap2
    
    # Handle missing data
    return 0, 0

def vcf_to_hap(vcf_file, output_prefix):
    """
    Convert phased VCF to SHAPEIT .hap and .sample files
    """
    samples = []
    hap_lines = []
    
    with open_file(vcf_file) as f:
        for line in f:
            line = line.strip()
            
            # Parse header to get sample names
            if line.startswith('#CHROM'):
                parts = line.split('\t')
                samples = parts[9:]  # Sample names start at column 9
                print(f"Found {len(samples)} samples")
                continue
            
            # Skip other header lines
            if line.startswith('#'):
                continue
            
            # Parse variant line
            parts = line.split('\t')
            chrom = parts[0]
            # If chromosome is '.', try to extract from variant ID or use 'CHR'
            if chrom == '.':
                # Check if rsID has chromosome info (e.g., rs123;17)
                if ';' in parts[2]:
                    chrom = parts[2].split(';')[-1]
                else:
                    chrom = 'CHR'  # Fallback - user will need to fix
            pos = parts[1]
            variant_id = parts[2] if parts[2] != '.' else f"{chrom}:{pos}"
            ref = parts[3]
            alt = parts[4]
            
            # Get format fields
            format_fields = parts[8].split(':')
            gp_idx = format_fields.index('GP') if 'GP' in format_fields else None
            gt_idx = format_fields.index('GT') if 'GT' in format_fields else None
            
            if gp_idx is None and gt_idx is None:
                print(f"Warning: No GT or GP field for variant {variant_id}")
                continue
            
            # Build haplotype line
            hap_data = [f"{chrom}:{pos}_{ref}_{alt}", variant_id, pos, ref, alt]
            
            # Parse each sample
            for sample_data in parts[9:]:
                sample_fields = sample_data.split(':')
                
                # Get GT and GP fields if they exist
                gt_field = sample_fields[gt_idx] if gt_idx is not None else None
                gp_field = sample_fields[gp_idx] if gp_idx is not None else None
                
                hap1, hap2 = parse_genotype(gt_field, gp_field)
                hap_data.extend([str(hap1), str(hap2)])
            
            hap_lines.append(' '.join(hap_data))
    
    # Write .hap file
    hap_file = f"{output_prefix}.hap"
    print(f"Writing {len(hap_lines)} variants to {hap_file}")
    with open(hap_file, 'w') as f:
        for line in hap_lines:
            f.write(line + '\n')
    
    # Write .sample file
    sample_file = f"{output_prefix}.sample"
    print(f"Writing {len(samples)} samples to {sample_file}")
    with open(sample_file, 'w') as f:
        f.write("ID_1 ID_2 missing\n")
        f.write("0 0 0\n")
        for sample in samples:
            f.write(f"{sample} {sample} 0\n")
    
    print("Conversion complete!")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python vcf_to_hap.py <input.vcf[.gz]> <output_prefix>")
        sys.exit(1)
    
    vcf_file = sys.argv[1]
    output_prefix = sys.argv[2]
    
    vcf_to_hap(vcf_file, output_prefix)
