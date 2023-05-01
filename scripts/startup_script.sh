#!/bin/bash
CONTAINER_ALREADY_STARTED="/db_created/CONTAINER_ALREADY_STARTED_PLACEHOLDER"
if [ ! -e $CONTAINER_ALREADY_STARTED ]; then
    set -e
    echo "-- First container startup --"
    sleep 15s
    python ddl_script.py
    python seed_script.py
    python downloader.py
    python extractor.py
    touch $CONTAINER_ALREADY_STARTED
else
    echo "-- Not first container startup --"
fi