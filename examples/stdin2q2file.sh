#!/usr/bin/env bash
if [ "$#" -ne 2 ]; then
    echo "Usage: stdin2q2file.sh <queue-name> <filepath>"
    exit
fi

python3 ../pipes/pipe.py processor pipes.processors.passthrough.PassThrough input rabbitmq localhost $1 output stream file $2 &
python3 ../pipes/pipe.py processor pipes.processors.passthrough.PassThrough input stream stdin output rabbitmq localhost $1
