#!/bin/bash
cd "$(dirname "$0")"
source tds_env/bin/activate
python3 bridges/tds_server.py
