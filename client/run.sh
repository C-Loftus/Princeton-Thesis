#!/bin/bash
set -e
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"/

# if -s is passed, run the server
if [ "$1" = "-s" ]; then
    echo "Starting server"
    ../server/.venv/bin/python ../server/server.py &
    sleep 3  # Sleep for 3s to give the server enough time to start
fi

for i in `seq 0 1`; do
    echo "Starting client $i"
    ./.venv/bin/python client.py &
done

# Enable CTRL+C to stop all background processes
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM
# Wait for all background processes to complete
wait
