#!/bin/bash

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the required packages
pip3 install -r requirements.txt

# Run the app (API)
python3 src/api/api_gateway.py
