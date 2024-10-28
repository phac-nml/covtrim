<table align="center" style="margin: 0px auto;">
  <tr>
    <td>
      <img src="https://raw.githubusercontent.com/phac-nml/covtrim/refs/heads/main/extra/covtrim-logo.svg" alt="covtrim Logo" width="400" height="auto"/>
    </td>
    <td>
      <h1>CovTrim: Coverage-Based Downsampling of FASTQ Files</h1>
<a href="https://anaconda.org/gosahan/covtrim">
  <img src="https://anaconda.org/gosahan/covtrim/badges/version.svg" alt="covtrim on Anaconda"/>
</a>
<a href="">
  <img src="https://anaconda.org/gosahan/covtrim/badges/platforms.svg"/>        
</a>
<a href="">
  <img src="https://anaconda.org/gosahan/covtrim/badges/latest_release_date.svg"/>        
</a>
    </td>
  </tr>
</table>

# CovTrim: Technical Documentation and Implementation Guide

## Table of Contents
1. [Introduction](#1-introduction)
2. [Installation](#2-installation)
3. [Mathematical Framework](#3-mathematical-framework)
4. [Implementation Details](#4-implementation-details)
5. [Usage Guide](#5-usage-guide)
6. [Output Files](#6-output-files)
7. [Performance Considerations](#7-performance-considerations)
8. [Support](#8-support)
9. [License](#9-license)

## 1. Introduction

CovTrim is a specialized bioinformatics tool designed for precise coverage-based downsampling of FASTQ files from amplicon sequencing data. It uses pysam for efficient FASTQ processing and implements robust algorithms for coverage calculation and read selection.

## 2. Installation

```bash
# Using conda
conda install -c gosahan covtrim

# Dependencies
- Python ≥ 3.7
- pandas
- numpy
- pysam
```

## 3. Mathematical Framework

### 3.1 Core Coverage Metrics

#### Theoretical Sequencing Space
The total sequencing space (TSS) is calculated based on the number of amplicons and their size:

$$TSS = N_a \times L_a$$

Where:
- $N_a$ = Number of amplicons
- $L_a$ = Amplicon length (bp)

Number of amplicons is calculated as:

$$N_a = \left\lceil \frac{G}{L_a} \right\rceil$$

Where:
- $G$ = Genome size (bp)

Code implementation:
```python
def calculate_amplicon_coverage(total_bases, num_amplicons, amplicon_size):
    sequencing_space = num_amplicons * amplicon_size  # TSS calculation
    # ...

# In downsample_fastq:
num_amplicons = np.ceil(genome_size / amplicon_size)  # Na calculation
```

#### Mean Coverage Depth
The mean coverage depth ($\bar{C}$) is calculated as:

$$\bar{C} = \frac{\sum_{i=1}^{n} l_i}{TSS}$$

Where:
- $l_i$ = Length of read $i$
- $n$ = Total number of reads
- $TSS$ = Theoretical sequencing space

Code implementation:
```python
def calculate_amplicon_coverage(total_bases, num_amplicons, amplicon_size):
    sequencing_space = num_amplicons * amplicon_size
    mean_coverage = total_bases / sequencing_space  # Mean coverage calculation
    # ...

# In downsample_fastq:
total_bases = df['len'].sum()  # Sum of all read lengths
```

#### Theoretical Reads per Amplicon
The expected number of reads per amplicon assuming uniform distribution:

$$R_{amplicon} = \frac{\sum_{i=1}^{n} l_i}{N_a \times L_a}$$

Code implementation:
```python
def calculate_amplicon_coverage(total_bases, num_amplicons, amplicon_size):
    theoretical_reads_per_amplicon = total_bases / (num_amplicons * amplicon_size)
```

### 3.2 Downsampling Calculations

#### Sampling Fraction
For a target coverage $C_t$, the sampling fraction ($f_s$) is calculated as:

$$f_s = \min(1, \frac{C_t}{\bar{C}})$$

Where:
- $C_t$ = Target coverage
- $\bar{C}$ = Current mean coverage

Code implementation:
```python
# In downsample_fastq:
sampling_fraction = min(1.0, target_coverage / current_coverage)
```

#### Expected Coverage After Sampling
The expected coverage after sampling ($C_e$) is:

$$C_e = f_s \times \bar{C} = \frac{\sum_{i \in S} l_i}{TSS}$$

Where:
- $S$ = Set of sampled reads
- $l_i$ = Length of read $i$

Code implementation:
```python
# In downsample_fastq:
sampled_bases = sampled_reads['len'].sum()
expected_coverage = sampled_bases / coverage_stats['sequencing_space']
```

### 3.3 Quality Control Metrics

#### Coverage Uniformity
Coverage uniformity is assessed using the coefficient of variation:

$$CV = \frac{\sigma_C}{\mu_C}$$

Where:
- $\sigma_C$ = Standard deviation of coverage
- $\mu_C$ = Mean coverage

#### Amplicon Representation
The representation of each amplicon is calculated as:

$$R_{amplicon} = \frac{N_{observed}}{N_{expected}}$$

Where:
- $N_{observed}$ = Observed number of reads per amplicon
- $N_{expected}$ = Expected number of reads based on uniform distribution

Code implementation:
```python
# These metrics are calculated and included in the final report
def calculate_amplicon_coverage(total_bases, num_amplicons, amplicon_size):
    # ...
    return {
        'mean_coverage': mean_coverage,
        'sequencing_space': sequencing_space,
        'theoretical_reads_per_amplicon': theoretical_reads_per_amplicon
    }
```

[Rest of the README remains the same...]

## Performance Analysis

### Time Complexity
The overall time complexity of the main operations:

$$T(n) = O(n \log n)$$

Where $n$ is the number of reads, due to sorting operations in the sampling process.

### Memory Complexity
The space complexity for the core operations:

$$M(n) = O(n)$$

Where $n$ is the number of reads, primarily from storing read identifiers.

### 4.2 Key Functions

#### calculate_amplicon_coverage
```python
def calculate_amplicon_coverage(total_bases, num_amplicons, amplicon_size):
    """
    Calculate coverage metrics for amplicon sequencing
    
    Returns:
    - mean_coverage
    - sequencing_space
    - theoretical_reads_per_amplicon
    """
```

#### downsample_fastq
```python
def downsample_fastq(input_fastq, target_coverage, output_dir, 
                    genome_size=16000, amplicon_size=500, random_seed=42):
    """
    Main function for FASTQ downsampling
    """
```

## 5. Usage Guide

### 5.1 Command Line Interface
```bash
covtrim -i <input.fastq> -o <output_dir> -tc <target_coverage> [options]

Required Arguments:
  -i, --input          Input FASTQ file
  -o, --output         Output directory
  -tc, --target-coverage  Target coverage depth (X)

Optional Arguments:
  -gs, --genome-size   Size of target genome (default: 16000 bp)
  -as, --amplicon-size Size of amplicons (default: 500 bp)
  -s, --seed          Random seed (default: 42)
```

### 5.2 Example Usage
```bash
# Basic usage
covtrim -i sample.fastq -o output_dir -tc 30

# Specify custom genome and amplicon size
covtrim -i sample.fastq -o output_dir -tc 30 -gs 29903 -as 400
```

## 6. Output Files

### 6.1 Directory Structure
```
coverage_<target>X/
├── <filename>_<target>X.fastq      # Downsampled FASTQ file
└── <filename>_<target>X_report.md  # Analysis report
```

### 6.2 Report Contents
- Analysis parameters
- Sequencing metrics
- Coverage calculations
- Sampling results
- Detailed methodology

## 7. Performance Considerations

### 7.1 Memory Usage
- Streaming FASTQ processing using pysam
- Only read headers stored in memory
- Linear memory complexity: O(n) where n is number of reads

### 7.2 Processing Speed
- Efficient indexing using pysam
- Fast random sampling with pandas
- Time complexity: O(n log n) for sorting operations

## 8. Support

For questions or issues, contact [Gurasis Osahan](mailto:gurasis.osahan@phac-aspc.gc.ca) at the National Microbiology Laboratory.

## 9. License

Licensed under Apache License, Version 2.0. See [LICENSE](http://www.apache.org/licenses/LICENSE-2.0) for details.

## Legal

**Copyright**: Government of Canada 

**Written by**: National Microbiology Laboratory, Public Health Agency of Canada

---

*Ensuring public health through advanced genomics. Developed with unwavering commitment and expertise by National Microbiology Laboratory, Public Health Agency of Canada.*
