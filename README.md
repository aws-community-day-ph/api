#!/bin/bash
# Script to activate the Python environment for the service
echo "Using this service's Python environment"
alias python=python3
python -m venv venv
. $PWD/venv/bin/activate
python -m pip install -r requirements.txt