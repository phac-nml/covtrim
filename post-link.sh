#!/bin/bash

set +e  

# Second installation block with conda
"${PREFIX}/bin/conda" install -c defaults -c conda-forge -c bioconda -c gosahan "samtools>=1.21" --yes

# Capture the exit code of the conda installation
conda_install_exit_code=$?

if [ $conda_install_exit_code -ne 0 ]; then
    echo "conda installation command exited with error code $conda_install_exit_code, but continuing script execution."
fi

# Python package installations
declare -a packages=(
    "setuptools"
    "typing_extensions"
    "wheel"
    "build"
    "pysam"
    "scipy"
    "pandas"
    "numpy"
)

for package in "${packages[@]}"; do
    echo "Attempting to install $package..."
    "${PREFIX}/bin/python" -m pip install $package
    pip_install_exit_code=$?

    if [ $pip_install_exit_code -ne 0 ]; then
        echo "Installation of $package exited with error code $pip_install_exit_code."
    else
        echo "Installation of $package completed successfully."
    fi
done