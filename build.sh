#!/bin/bash

# Exit on error, but not on failed pip install
set -e

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
    "numpy>=1.21.2"  # Install numpy before scipy and pandas
    "scipy>=1.7.1"
    "pandas>=1.3.3"
    "pysam>=0.22.0"
)

# Install each package
echo "Installing dependencies..."
for package in "${packages[@]}"; do
    install_package "$package"
done

# Install the actual package using pip, with a fallback to setup.py
echo "Installing covtrim..."
if $PYTHON -m pip install . --no-deps -vv; then
    echo "✓ covtrim installed successfully with pip."
else
    echo "⚠ pip installation failed; attempting installation with setup.py..."
    if $PYTHON setup.py install; then
        echo "✓ covtrim installed successfully with setup.py."
    else
        echo "Error: Both pip and setup.py installations failed."
        exit 1
    fi
fi

# Verify installation
echo "Verifying installation..."
if $PYTHON -c "import covtrim; print(f'CovTrim version: {covtrim.__version__}')"; then
    echo "✓ CovTrim installation verified successfully."
else
    echo "Error: Failed to import covtrim after installation"
    exit 1
fi
