#!/bin/bash

# Exit on error, but not on failed pip install
set -e

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
    "setuptools"
    "typing_extensions"
    "wheel"
    "build"
    "numpy"  
    "scipy"
    "pandas"
    "pysam"
)

# Install each package
echo "Installing dependencies..."
for package in "${packages[@]}"; do
    install_package "$package"
done

# Install the actual package
echo "Installing covtrim..."
$PYTHON -m pip install . --no-deps -vv || {
    echo "Error: Failed to install covtrim package"
    exit 1
}

# Verify installation
echo "Verifying installation..."
if $PYTHON -c "import covtrim; print(f'CovTrim version: {covtrim.__version__}')"; then
    echo "✓ CovTrim installation verified successfully."
else
    echo "Error: Failed to import covtrim after installation"
    exit 1
fi