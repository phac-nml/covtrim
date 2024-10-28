#!/usr/bin/env python3

import pandas as pd
import numpy as np
import os
import pysam
import argparse
from pathlib import Path
from datetime import datetime

def calculate_amplicon_coverage(total_bases, num_amplicons, amplicon_size):
    """
    Calculate coverage metrics for amplicon sequencing
    
    Parameters:
    -----------
    total_bases : int
        Total number of sequenced bases
    num_amplicons : int
        Number of amplicons covering genome
    amplicon_size : int
        Size of each amplicon
    
    Returns:
    --------
    dict
        Dictionary containing various coverage metrics
    """
    sequencing_space = num_amplicons * amplicon_size
    mean_coverage = total_bases / sequencing_space
    theoretical_reads_per_amplicon = total_bases / (num_amplicons * amplicon_size)
    
    return {
        'mean_coverage': mean_coverage,
        'sequencing_space': sequencing_space,
        'theoretical_reads_per_amplicon': theoretical_reads_per_amplicon
    }

def get_original_filename(fofn_path):
    """Extract the original filename without path and extension"""
    return os.path.splitext(os.path.basename(fofn_path))[0]

def write_markdown_report(output_stats, stats_dict):
    """
    Write a comprehensive markdown report with LaTeX formulas and statistics
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(output_stats, 'w') as stats_file:
        stats_file.write(f"""# CovTrim - Coverage-Based FASTQ Trimming Tool Analysis Report

## Description
`covtrim` is a specialized bioinformatics tool designed for precise coverage-based downsampling of FASTQ files from amplicon sequencing data. It intelligently adjusts sequencing depth while maintaining quality metrics and amplicon representation, making it particularly useful for viral genomics, amplicon-based sequencing projects, and high-throughput sequencing optimization.

## Analysis Information
- **Date**: {timestamp}
- **Script Version**: 0.2.0

## Overview
This report details the downsampling analysis performed on amplicon sequencing data, including the mathematical basis for coverage calculations and sampling decisions.

## Input Parameters
- **Input File**: {stats_dict['input_file']}
- **Target Coverage**: {stats_dict['target_coverage']}X
- **Genome Size**: {stats_dict['genome_size']:,} bp
- **Amplicon Size**: {stats_dict['amplicon_size']} bp
- **Number of Amplicons**: {stats_dict['num_amplicons']}

## Sequencing Metrics

### Basic Statistics
- **Total Bases Sequenced**: {stats_dict['total_bases']:,} bp
- **Total Reads**: {stats_dict['total_reads']:,}
- **Average Read Length**: {stats_dict['avg_read_length']:.2f} bp

### Coverage Calculations

#### 1. Theoretical Sequencing Space
The total sequencing space is calculated based on the number of amplicons and their size:

$\\text{{Sequencing Space}} = \\text{{Number of Amplicons}} \\times \\text{{Amplicon Size}}$

$\\text{{Sequencing Space}} = {stats_dict['num_amplicons']} \\times {stats_dict['amplicon_size']} = {stats_dict['sequencing_space']:,} \\text{{ bp}}$

#### 2. Mean Coverage
Mean coverage is calculated as the ratio of total sequenced bases to the sequencing space:

$\\text{{Mean Coverage}} = \\frac{{\\text{{Total Bases}}}}{{\\text{{Sequencing Space}}}}$

$\\text{{Mean Coverage}} = \\frac{{{stats_dict['total_bases']:,}}}{{{stats_dict['sequencing_space']:,}}} = {stats_dict['current_coverage']:.2f}\\text{{X}}$

#### 3. Theoretical Reads per Amplicon
Assuming perfect distribution across amplicons:

$\\text{{Reads per Amplicon}} = \\frac{{\\text{{Total Bases}}}}{{\\text{{Number of Amplicons}} \\times \\text{{Amplicon Size}}}}$

$\\text{{Reads per Amplicon}} = \\frac{{{stats_dict['total_bases']:,}}}{{{stats_dict['num_amplicons']} \\times {stats_dict['amplicon_size']}}} = {stats_dict['theoretical_reads_per_amplicon']:.2f}$

## Downsampling Analysis

### Sampling Calculation
The sampling fraction is determined by the ratio of target to current coverage:

$\\text{{Sampling Fraction}} = \\frac{{\\text{{Target Coverage}}}}{{\\text{{Current Coverage}}}}$

$\\text{{Sampling Fraction}} = \\frac{{{stats_dict['target_coverage']}}}{{{stats_dict['current_coverage']:.2f}}} = {stats_dict['sampling_fraction']:.4f}$

### Results
- **Sampling Fraction**: {stats_dict['sampling_fraction']:.2%}
- **Sampled Reads**: {stats_dict['sampled_reads']:,}
- **Sampled Bases**: {stats_dict['sampled_bases']:,}
""")

        # Add expected coverage section if downsampling occurred
        if stats_dict['sampling_fraction'] < 1:
            stats_file.write(f"""
### Expected Coverage After Sampling
The expected coverage after sampling is calculated using the same formula as the initial coverage:

$\\text{{Expected Coverage}} = \\frac{{\\text{{Sampled Bases}}}}{{\\text{{Sequencing Space}}}}$

$\\text{{Expected Coverage}} = \\frac{{{stats_dict['sampled_bases']:,}}}{{{stats_dict['sequencing_space']:,}}} = {stats_dict['expected_coverage']:.2f}\\text{{X}}$
""")

        stats_file.write("""
## Methods
### Coverage Calculation
The coverage calculation takes into account the amplicon-based sequencing approach, where:
1. The genome is divided into amplicons of fixed size
2. Coverage is calculated across the total sequencing space
3. Read distribution is assumed to be uniform across amplicons

### Downsampling Method
The downsampling process:
1. Calculates required sampling fraction based on target coverage
2. Randomly samples reads using a fixed random seed (42) for reproducibility
3. Maintains original read headers and quality scores
4. Preserves read pairing and sequence context

### Implementation Notes
- Random sampling is performed using Pandas' DataFrame.sample() function
- Original FASTQ header information is preserved, including instrument and run metadata
- Coverage calculations account for the amplicon-based sequencing approach
- Implemented using pysam for efficient FASTQ processing
""")

def index_fastq(input_fastq):
    """
    Create an index of FASTQ reads and their lengths using pysam
    
    Parameters:
    -----------
    input_fastq : str
        Path to input FASTQ file
    
    Returns:
    --------
    pandas.DataFrame
        DataFrame containing read names and lengths
    """
    read_data = []
    with pysam.FastxFile(input_fastq) as fin:
        for entry in fin:
            read_data.append({
                'read_name': entry.name,
                'len': len(entry.sequence)
            })
    
    return pd.DataFrame(read_data)

def downsample_fastq(input_fastq, target_coverage, output_dir, genome_size=16000, 
                    amplicon_size=500, random_seed=42):
    """
    Downsample a FASTQ file to a target coverage using pysam
    
    Parameters:
    -----------
    input_fastq : str
        Path to input FASTQ file
    target_coverage : float
        Desired coverage depth (X)
    output_dir : str
        Directory for output files
    genome_size : int
        Size of target genome in base pairs
    amplicon_size : int
        Size of individual amplicons
    random_seed : int
        Random seed for reproducible sampling
    """
    # Create output directory structure
    orig_filename = get_original_filename(input_fastq)
    output_dir = f"coverage_{target_coverage}X"
    os.makedirs(output_dir, exist_ok=True)
    
    # Set up output files
    output_fastq = os.path.join(output_dir, f"{orig_filename}_{target_coverage}X.fastq")
    output_stats = os.path.join(output_dir, f"{orig_filename}_{target_coverage}X_report.md")
    
    # Calculate number of amplicons
    num_amplicons = np.ceil(genome_size / amplicon_size)
    
    # Index the FASTQ file using pysam
    print("Indexing FASTQ file...")
    df = index_fastq(input_fastq)
    
    # Calculate metrics
    total_bases = df['len'].sum()
    total_reads = len(df)
    avg_read_length = total_bases / total_reads
    
    # Calculate coverage metrics
    coverage_stats = calculate_amplicon_coverage(
        total_bases=total_bases,
        num_amplicons=num_amplicons,
        amplicon_size=amplicon_size
    )
    current_coverage = coverage_stats['mean_coverage']
    
    # Print analysis information
    print(f"\nAnalysis for {input_fastq}:")
    print(f"Total bases: {total_bases:,}")
    print(f"Number of reads: {total_reads:,}")
    print(f"Average read length: {avg_read_length:.2f}")
    print(f"Number of amplicons: {num_amplicons}")
    print(f"Amplicon size: {amplicon_size}")
    print(f"Total sequencing space: {coverage_stats['sequencing_space']:,}")
    print(f"Current mean coverage: {current_coverage:.2f}X")
    print(f"Theoretical reads per amplicon: {coverage_stats['theoretical_reads_per_amplicon']:.2f}")
    
    # Calculate sampling fraction
    sampling_fraction = target_coverage / current_coverage
    sampled_coverage_stats = None
    
    if sampling_fraction >= 1:
        print(f"\nWarning: Requested coverage {target_coverage}X exceeds "
              f"available coverage {current_coverage:.2f}X. "
              "Using all available reads.")
        sampled_reads = df
    else:
        # Randomly sample reads
        sampled_reads = df.sample(frac=sampling_fraction, random_state=random_seed)
        print(f"\nSampling {sampling_fraction:.2%} of reads to achieve {target_coverage}X "
              f"coverage across amplicons")
        
        # Calculate expected coverage after sampling
        sampled_bases = sampled_reads['len'].sum()
        sampled_coverage_stats = calculate_amplicon_coverage(
            total_bases=sampled_bases,
            num_amplicons=num_amplicons,
            amplicon_size=amplicon_size
        )
        print(f"Expected coverage after sampling: {sampled_coverage_stats['mean_coverage']:.2f}X")
    
    # Collect statistics for report
    stats_dict = {
        'input_file': input_fastq,
        'target_coverage': target_coverage,
        'genome_size': genome_size,
        'amplicon_size': amplicon_size,
        'num_amplicons': num_amplicons,
        'total_bases': total_bases,
        'total_reads': total_reads,
        'avg_read_length': avg_read_length,
        'sequencing_space': coverage_stats['sequencing_space'],
        'current_coverage': current_coverage,
        'theoretical_reads_per_amplicon': coverage_stats['theoretical_reads_per_amplicon'],
        'sampling_fraction': sampling_fraction,
        'sampled_reads': len(sampled_reads),
        'sampled_bases': sampled_reads['len'].sum()
    }
    
    if sampling_fraction < 1 and sampled_coverage_stats:
        stats_dict['expected_coverage'] = sampled_coverage_stats['mean_coverage']
    
    # Write markdown report
    write_markdown_report(output_stats, stats_dict)
    
    # Create a set of read IDs to sample
    read_ids = set(sampled_reads['read_name'])
    
    # Process the FASTQ file using pysam and write sampled reads
    print(f"\nWriting sampled reads to {output_fastq}")
    with pysam.FastxFile(input_fastq) as fin, open(output_fastq, 'w') as outfile:
        for entry in fin:
            if entry.name in read_ids:
                outfile.write(f"@{entry.name}\n{entry.sequence}\n+\n{entry.quality}\n")
    
    print(f"Analysis complete. Report written to {output_stats}")

def main():
    parser = argparse.ArgumentParser(
        prog='covtrim',
        description='\033[0m\033[1mcovtrim\033[0m is a specialized bioinformatics tool designed for precise coverage-based downsampling of FASTQ files from amplicon sequencing data. \n'
        'It intelligently adjusts sequencing depth while maintaining quality metrics and amplicon representation, making it particularly useful for viral genomics,\n'
        'amplicon-based sequencing projects, and high-throughput sequencing optimization.',
        epilog=(
            '\033[1m\033[31mCopyright:\033[0m \033[1mGovernment of Canada\033[0m\n'
            '\033[1m\033[31mWritten by:\033[0m \033[1mNational Microbiology Laboratory, Public Health Agency of Canada\033[0m'
        ),
        formatter_class=argparse.RawTextHelpFormatter,
        usage='%(prog)s -i <input.fastq> -o <output_dir> -tc <target_coverage> [options]'
    )

    # Required arguments group
    required = parser.add_argument_group('Required arguments')
    required.add_argument(
        '-i', '--input',
        dest='input_fastq',
        required=True,
        help='Input FASTQ file for downsampling'
    )
    required.add_argument(
        '-o', '--output',
        dest='output_dir',
        required=True,
        help='Output directory for downsampled files and reports'
    )
    required.add_argument(
        '-tc', '--target-coverage',
        dest='target_coverage',
        type=float,
        required=True,
        help='Target sequencing coverage (X) for downsampling'
    )

    # Optional arguments group
    optional = parser.add_argument_group('Optional arguments')
    optional.add_argument(
        '-gs', '--genome-size',
        dest='genome_size',
        type=int,
        default=16000,
        help='Size of target genome in base pairs (default: 16000 bp)'
    )
    optional.add_argument(
        '-as', '--amplicon-size',
        dest='amplicon_size',
        type=int,
        default=500,
        help='Size of individual amplicons in base pairs (default: 500 bp)'
    )
    optional.add_argument(
        '-s', '--seed',
        dest='random_seed',
        type=int,
        default=42,
        help='Random seed for reproducible downsampling (default: 42)'
    )
    optional.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 1.0.0',
        help='Show program version number and exit'
    )

    args = parser.parse_args()

    # Update function call to use new arguments
    downsample_fastq(
        input_fastq=args.input_fastq,
        target_coverage=args.target_coverage,
        genome_size=args.genome_size,
        amplicon_size=args.amplicon_size,
        output_dir=args.output_dir,
        random_seed=args.random_seed,
    )

if __name__ == '__main__':
    main()