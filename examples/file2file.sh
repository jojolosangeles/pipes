#!/usr/bin/env bash
if [ "$#" -ne 2 ]; then
    echo "Usage: file2file.sh <infile> <outfile>"
    exit
fi
python3 ../pipes/pipe.py input stream file $1 output stream file $2
