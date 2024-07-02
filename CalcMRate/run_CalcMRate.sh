#!/bin/bash

# Set the Python file path
PYTHON_FILE="CalcMRate.py"

# Get the parameters from the command line
PARAMS="$@"

# Run the Python script and pass the parameters
python3 "$PYTHON_FILE" $PARAMS
