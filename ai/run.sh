#!/bin/bash

# Create generated_pdfs directory if it doesn't exist
mkdir -p generated_pdfs

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the required packages
pip3 install -r requirements.txt

# Run the app (API)
python3 src/api_gateway.py
