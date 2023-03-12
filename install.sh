#!/bin/bash
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "Python venv could not be found, please install before running this script."
    exit
fi

source venv/bin/activate

python -m pip install -U pygame==2.2.0
