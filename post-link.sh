#!/bin/bash

set +e  

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