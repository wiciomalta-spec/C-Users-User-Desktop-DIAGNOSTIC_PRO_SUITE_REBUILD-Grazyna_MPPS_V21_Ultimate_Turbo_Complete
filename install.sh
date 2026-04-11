#!/bin/bash

echo "============================================================"
echo "DIAGNOSTIC PRO SUITE ULTIMATE EDITION INSTALLER"
echo "Version: 2.0.0"
echo "============================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check Python version
python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"
if [ $? -ne 0 ]; then
    echo "ERROR: Python 3.8 or higher is required"
    exit 1
fi

echo "Starting Python installer..."
python3 install.py

if [ $? -ne 0 ]; then
    echo "Installation failed!"
    exit 1
fi

echo ""
echo "Installation completed successfully!"
echo ""
