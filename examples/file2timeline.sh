#!/usr/bin/env bash
if [ "$#" -ne 1 ]; then
    echo "Usage: file2timeline.sh <json file>"
    exit
fi
python3 ../pipes/pipe.py processor timelines.timeline_engine.TimelineEngine input stream file $1 output stream stdout
