#!/usr/bin/env bash
if [ "$#" -ne 2 ]; then
    echo "Usage: file2timeline.sh <json file> <gist filename>"
    exit
fi
python3 ../pipes/pipe.py processor timelines.timeline_engine.TimelineEngine input stream file $1 output gist $2
