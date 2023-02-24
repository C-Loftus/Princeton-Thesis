#!/bin/bash
set -e
echo " Script running at $(pwd)"
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"/

# if -s is passed, run the server
if [ "$1" = "-s" ]; then
    echo "Starting server"
    .../server/.venv/bin/python ../server/server.py &
    sleep 3  # Sleep for 3s to give the server enough time to start
fi
curl localhost:5000/start
for i in `seq 0 1 10`; do
    echo "Starting client $i"
    sleep 1
    ../.venv/bin/python ../training.py &
done

# Enable CTRL+C to stop all background processes
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM
# Wait for all background processes to complete
wait
echo "Stopping flwr server"
curl localhost:5000/stop
