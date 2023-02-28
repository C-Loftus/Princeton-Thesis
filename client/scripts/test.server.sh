#!/bin/bash
set -e
echo " Script running at $(pwd)"
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"/

# if -s is included in any position, start the server
if [[ "$*" == *"-s"* ]]; then
    echo "Starting server"
    ../../server/.venv/bin/python ../../server/server.py &
    sleep 3  # Sleep for 3s to give the server enough time to start
fi

curl localhost:5000/start