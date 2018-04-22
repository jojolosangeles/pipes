#!/usr/bin/env bash
if [ "$#" -ne 1 ]; then
    echo "Usage: stdin2file.sh <filepath>"
    exit
fi
python3 ../pipes/pipe.py processor pipes.processors.passthrough.PassThrough input stream stdin output stream stdout output stream file $1
