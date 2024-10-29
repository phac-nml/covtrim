#!/bin/bash

# Exit on error, but not on failed pip install
set -e

# Function to write messages to $PREFIX/.messages.txt
log_message() {
    echo "$1" >> "$PREFIX/.messages.txt"
}

# Function to execute command and redirect output to messages file
execute_command() {
    local cmd="$1"
    local output
    output=$($cmd 2>&1)
    log_message "$output"
    return ${PIPESTATUS[0]}
}

# Fail-safe: Check if Python or Python3 is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    log_message "Error: Python or Python3 not found. Please install Python to proceed."
    exit 1
fi

# Define PYTHON executable if not already set
PYTHON=${PYTHON:-python3}  # Use 'python3' or your preferred version

# Function to install a Python package with error handling
install_package() {
    local package=$1
    log_message "Attempting to install $package..."
    
    if execute_command "$PYTHON -m pip install $package --no-input"; then
        log_message "✓ Installation of $package completed successfully."
        return 0
    else
        log_message "⚠ Warning: Installation of $package failed, continuing anyway..."
        return 0  # Don't fail on pip install errors
    fi
}

# Required packages in order of dependency
declare -a packages=(
    "setuptools>=65.0.0"
    "typing_extensions>=4.0.0"
    "wheel>=0.44.0"
    "build>=1.0.0"
    "numpy=1.24.3"
    "pandas=1.5.3"
    "pysam>=0.20.0"
)

# Install each package
log_message "Installing dependencies..."
for package in "${packages[@]}"; do
    install_package "$package"
done

# Install the actual package using poetry first, setup.py second, and pip as fallback
log_message "Installing covtrim..."
if command -v poetry &> /dev/null; then
    log_message "Poetry found, attempting to install with poetry..."
    if execute_command "poetry lock && poetry install"; then
        log_message "✓ covtrim installed successfully with poetry."
    else
        log_message "⚠ Poetry installation failed; attempting installation with setup.py..."
        if execute_command "$PYTHON setup.py install --no-input"; then
            log_message "✓ covtrim installed successfully with setup.py."
        else
            log_message "⚠ setup.py installation failed; attempting installation with pip..."
            if execute_command "$PYTHON -m pip install . --no-deps -vv --no-input"; then
                log_message "✓ covtrim installed successfully with pip."
            else
                log_message "Error: All installation methods (poetry, setup.py, pip) failed."
                exit 1
            fi
        fi
    fi
else
    log_message "Poetry not found; attempting installation with setup.py..."
    if execute_command "$PYTHON setup.py install --no-input"; then
        log_message "✓ covtrim installed successfully with setup.py."
    else
        log_message "⚠ setup.py installation failed; attempting installation with pip..."
        if execute_command "$PYTHON -m pip install . --no-deps -vv --no-input"; then
            log_message "✓ covtrim installed successfully with pip."
        else
            log_message "Error: Both setup.py and pip installations failed."
            exit 1
        fi
    fi
fi