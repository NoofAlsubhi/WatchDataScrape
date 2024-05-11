#!/bin/bash

# Update the package lists for apt
sudo apt update -y

# Install required system packages: Python 3 and pip
sudo apt install python3 python3-pip -y

# Install Python 3.10 virtual environment package
sudo apt install python3.10-venv -y

# Create a virtual environment named 'venv'
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install Python dependencies using pip from the requirements.txt file
pip install -r requirements.txt

# Deactivate the virtual environment
deactivate
