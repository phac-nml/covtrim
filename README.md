<table align="center" style="margin: 0px auto;">
  <tr>
    <td>
      <img src="https://raw.githubusercontent.com/phac-nml/covtrim/main/extra/covtrim_logo.svg" alt="covtrim Logo" width="400" height="auto"/>
    </td>
    <td>
      <h1>Nanopore Genome Optimization Bioinformatics Pipeline</h1>
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

# covtrim - Intelligent Coverage-Based FASTQ Trimming Tool

## Description
`covtrim` is a specialized bioinformatics tool designed for precise coverage-based downsampling of FASTQ files from amplicon sequencing data. It intelligently adjusts sequencing depth while maintaining quality metrics and amplicon representation, making it particularly useful for viral genomics, amplicon-based sequencing projects, and high-throughput sequencing optimization.

## Key Features
- Smart coverage calculation based on amplicon architecture
- Quality-aware read selection
- Comprehensive QC metrics generation
- Support for both targeted and whole-genome amplicon sequencing
- Detailed markdown reports with sequencing metrics
- Memory-efficient processing of large FASTQ files
- Built-in GC content and quality score analysis
- Reproducible downsampling with fixed random seed

## Use Cases
1. **Viral Genome Sequencing**
   - Normalize coverage across samples
   - Optimize sequencing depth for variant calling
   - Reduce computational requirements for downstream analysis

2. **Amplicon-Based Projects**
   - Balance coverage across multiple samples
   - Reduce storage requirements
   - Standardize inputs for analysis pipelines

3. **Method Development**
   - Test coverage requirements
   - Optimize sequencing protocols
   - Validate analysis pipelines

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