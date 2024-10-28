<table align="center" style="margin: 0px auto;">
  <tr>
    <td>
      <img src="https://raw.githubusercontent.com/phac-nml/covtrim/main/extra/covtrim_logo.svg" alt="covtrim Logo" width="400" height="auto"/>
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

# CovTrim: Technical Documentation and Mathematical Foundations

## Table of Contents
1. Introduction
2. Mathematical Framework
3. Implementation Details
4. Coverage Calculations
5. Quality Control Metrics
6. Performance Analysis

## 1. Introduction

CovTrim is a specialized bioinformatics tool designed for precise coverage-based downsampling of FASTQ files from amplicon sequencing data. This documentation details the mathematical foundations and algorithms used in the coverage calculations and downsampling procedures.

## 2. Mathematical Framework

### 2.1 Core Coverage Calculations

#### Theoretical Sequencing Space
The fundamental unit of calculation is the theoretical sequencing space (TSS), defined as:

$TSS = N_a \times L_a$

Where:
- $N_a$ = Number of amplicons = $\ceil{\frac{G}{L_a}}$
- $G$ = Genome size (bp)
- $L_a$ = Amplicon length (bp)

#### Mean Coverage Depth
The mean coverage depth ($\bar{C}$) is calculated as:

$\bar{C} = \frac{\sum_{i=1}^{n} l_i}{TSS}$

Where:
- $l_i$ = Length of read $i$
- $n$ = Total number of reads

### 2.2 Downsampling Calculations

#### Sampling Fraction
For a target coverage $C_t$, the sampling fraction ($f_s$) is:

$f_s = \min(1, \frac{C_t}{\bar{C}})$

#### Expected Coverage After Sampling
The expected coverage after sampling ($C_e$) is:

$C_e = f_s \times \bar{C}$

## 3. Implementation Details

### 3.1 Read Selection Algorithm
```python
def calculate_sampling_fraction(current_coverage, target_coverage):
    return min(1.0, target_coverage / current_coverage)
```

### 3.2 Quality-Aware Sampling
The tool implements quality-aware sampling through:

$Q_{read} = \frac{1}{L}\sum_{i=1}^{L} q_i$

Where:
- $L$ = Read length
- $q_i$ = Quality score at position $i$

## 4. Coverage Calculations

### 4.1 Amplicon-Specific Considerations
For tiling amplicon designs, coverage is calculated per amplicon region:

$C_{amplicon} = \frac{\sum_{r \in R_a} l_r}{L_a}$

Where:
- $R_a$ = Reads mapping to amplicon $a$
- $l_r$ = Length of read $r$

### 4.2 Genome-Wide Coverage
The genome-wide coverage estimate accounts for amplicon overlap:

$C_{genome} = \frac{\sum_{a=1}^{N_a} C_{amplicon}(a) \times L_a}{G}$

## 5. Quality Control Metrics

### 5.1 Coverage Uniformity
Coverage uniformity is assessed using the coefficient of variation:

$CV = \frac{\sigma_C}{\mu_C}$

Where:
- $\sigma_C$ = Standard deviation of coverage
- $\mu_C$ = Mean coverage

### 5.2 Amplicon Representation
Amplicon representation is quantified as:

$R_{amplicon} = \frac{N_{observed}}{N_{expected}}$

## 6. Performance Analysis

### 6.1 Memory Usage
Memory complexity: $O(n)$ where $n$ is the number of reads

### 6.2 Time Complexity
Processing time: $O(n \log n)$ for sorting and sampling operations

## Appendix A: Command Line Interface

```bash
covtrim -i input.fastq -o output_dir -tc target_coverage [options]
```
## Usage
```bash
covtrim <input.fastq> <target_coverage> [options]

Required Arguments:
  input.fastq       Input FASTQ file
  target_coverage   Desired coverage depth (X)

Optional Arguments:
  --genome-size     Size of target genome in base pairs (default: 16000)
  --amplicon-size   Size of individual amplicons (default: 500)
  --min-quality     Minimum quality score for reads (default: None)
  --seed           Random seed for reproducibility (default: 42)
```

Note: All calculations are performed using double-precision floating-point arithmetic to ensure numerical stability and accuracy.