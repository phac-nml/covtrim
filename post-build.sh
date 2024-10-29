#!/bin/bash

# Exit on error, but not on failed pip install
set -e

# Fail-safe: Check if Python or Python3 is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "Error: Python or Python3 not found. Please install Python to proceed."
    exit 1
fi

# Define PYTHON executable if not already set
PYTHON=${PYTHON:-python3}  # Use 'python3' or your preferred version

# Function to install a Python package with error handling
install_package() {
    local package=$1
    echo "Attempting to install $package..."

    if $PYTHON -m pip install $package; then
        echo "✓ Installation of $package completed successfully."
    else
        echo "⚠ Warning: Installation of $package failed, continuing anyway..."
    fi
}

# Required packages in order of dependency
declare -a packages=(
    "setuptools>=65.0.0"
    "typing_extensions>=4.0.0"
    "wheel>=0.44.0"
    "build>=1.0.0"
    "numpy>=1.21.2"
    "scipy>=1.7.1"
    "pandas>=1.3.3"
    "pysam>=0.22.0"
)

# Install each package
echo "Installing dependencies..."
for package in "${packages[@]}"; do
    install_package "$package"
done

# Install the actual package using poetry first, setup.py second, and pip as fallback
echo "Installing covtrim..."
if command -v poetry &> /dev/null; then
    echo "Poetry found, attempting to install with poetry..."
    if poetry lock && poetry install; then
        echo "✓ covtrim installed successfully with poetry."
    else
        echo "⚠ Poetry installation failed; attempting installation with setup.py..."
        if $PYTHON setup.py install; then
            echo "✓ covtrim installed successfully with setup.py."
        else
            echo "⚠ setup.py installation failed; attempting installation with pip..."
            if $PYTHON -m pip install . --no-deps -vv; then
                echo "✓ covtrim installed successfully with pip."
            else
                echo "Error: All installation methods (poetry, setup.py, pip) failed."
                exit 1
            fi
        fi
    fi
else
    echo "Poetry not found; attempting installation with setup.py..."
    if $PYTHON setup.py install; then
        echo "✓ covtrim installed successfully with setup.py."
    else
        echo "⚠ setup.py installation failed; attempting installation with pip..."
        if $PYTHON -m pip install . --no-deps -vv; then
            echo "✓ covtrim installed successfully with pip."
        else
            echo "Error: Both setup.py and pip installations failed."
            exit 1
        fi
    fi
fi
