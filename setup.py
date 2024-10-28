#!/usr/bin/env python3
import setuptools

# Project metadata
NAME = "covtrim"
VERSION = "0.1.0"
AUTHOR = "Gurasis Osahan"
AUTHOR_EMAIL = "gurasis.osahan@phac-aspc.gc.ca"
DESCRIPTION = "CovTrim is a specialized bioinformatics tool designed for precise coverage-based downsampling of FASTQ files from amplicon sequencing data."
LONG_DESCRIPTION = """
CovTrim is a specialized bioinformatics tool designed for precise coverage-based downsampling of FASTQ files from amplicon sequencing data. 
It intelligently adjusts sequencing depth while maintaining quality metrics and amplicon representation, making it particularly useful for 
viral genomics, amplicon-based sequencing projects, and high-throughput sequencing optimization.
"""
URL = "https://github.com/phac-nml/covtrim"
LICENSE = "Apache License, Version 2.0"

# Define project dependencies
DEPENDENCIES = [
    "pysam",
    "numpy",
    "scipy",
    "pandas",
]

ENTRY_POINTS = {
    "console_scripts": [
        "covtrim=covtrim.covtrim:main"
    ]
}

# Project classifiers
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: Apache Software License',
    'Environment :: Console',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
]

PROJECT_URLS = {
    "Documentation": "https://github.com/phac-nml/covtrim/blob/main/README.md",
    "Source Code": "https://github.com/phac-nml/covtrim",
    "Issue Tracker": "https://github.com/phac-nml/covtrim/issues",
    "Examples": "https://github.com/phac-nml/covtrim/tree/main/examples",
    "FAQ": "https://github.com/phac-nml/covtrim/wiki/FAQ",
    "License": "https://github.com/phac-nml/covtrim/blob/main/LICENSE"
}

setuptools.setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    license=LICENSE,
    install_requires=DEPENDENCIES,
    entry_points=ENTRY_POINTS,
    classifiers=CLASSIFIERS,
    python_requires='>=3.8,<=3.11',
    keywords="bioinformatics genomics NGS pipeline coverage trimming FASTQ",
    project_urls=PROJECT_URLS,
    packages=setuptools.find_packages(),  # Changed from find_namespace_packages
    include_package_data=True,
    platforms='linux',
    zip_safe=False,
)