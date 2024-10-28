#!/usr/bin/env python3
import setuptools

# Project metadata
name = "covtrim"
version = "0.1.0"
author = "Gurasis Osahan"
author_email = "gurasis.osahan@phac-aspc.gc.ca"
description = "CovTrim is a specialized bioinformatics tool designed for precise coverage-based downsampling of FASTQ files from amplicon sequencing data."
long_description = """
CovTrim is a specialized bioinformatics tool designed for precise coverage-based downsampling of FASTQ files from amplicon sequencing data. It intelligently adjusts sequencing depth while maintaining quality metrics and amplicon representation, making it particularly useful for viral genomics, amplicon-based sequencing projects, and high-throughput sequencing optimization.
"""
url = "https://github.com/phac-nml/covtrim"
license_type = "Apache License, Version 2.0"

# Define project dependencies
dependencies = [
    'wheel',
    "pip",
    "build",
    "pysam",
    "numpy",
    "scipy",
    "pandas",
]

entry_points = {"console_scripts": ["covtrim=covtrim.covtrim_main:main"]}

# Project classifiers (https://pypi.org/classifiers/)
classifiers=[
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Science/Research",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
]

# Additional project information
keywords = "Bioinformatics genomics NGS pipeline"
project_urls = {
    "Documentation": "https://github.com/phac-nml/covtrim/raw/branch/main/README.md",
    "Source Code": "https://github.com/phac-nml/covtrim",
    "Issue Tracker": "https://github.com/phac-nml/covtrim/issues",
    "Examples": "https://github.com/phac-nml/covtrim/examples",
    "FAQ": "https://github.com/phac-nml/covtrim/wiki/FAQ",
    "License": "https://github.com/phac-nml/covtrim/raw/branch/main/LICENSE"
}

# Package configuration
setuptools.setup(
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=url,
    license=license_type,
    install_requires=dependencies,
    entry_points=entry_points,
    classifiers=classifiers,
    python_requires='<=3.11',
    keywords=keywords,
    project_urls=project_urls,
    include_package_data=True,
    platforms='any',
    zip_safe=False,
)
