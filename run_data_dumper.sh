#!/bin/bash

echo "Running Bash script..."

rm token.json
rm sheet_token.json

echo "Executing Python script..."

python3 -m venv venv


echo "Entering venv..."
source venv/bin/activate
echo "installing required libraries..."

pip install -r requirements.txt

echo "running program..."
python3 main.py

echo "program finished running, removing venv..."

rm -rf venv