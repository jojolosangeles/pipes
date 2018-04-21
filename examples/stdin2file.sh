#!/usr/bin/env bash
if [ "$#" -ne 1 ]; then
    echo "Usage: stdin2file.sh <filepath>"
    exit
fi
python3 ../pipes/pipe.py input stream stdin output stream file $1