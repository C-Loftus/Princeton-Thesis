#!/bin/bash
set -e
echo " Script running at $(pwd)"
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# if -s is included in any position, start the server
if [[ "$*" == *"-s"* ]]; then
    # try catch fuser -k 5000/tcp
    fuser -k 5000/tcp || true
    echo "Starting server"
    ../../server/.venv/bin/python ../../server/server.py &
    sleep 3  # Sleep for 3s to give the server enough time to start
fi

curl localhost:5000/start

args=""
# if -t is included in any position, run with talon data
if [[ "$*" == *"-t"* ]]; then
    args="--talon"
    echo "Running with talon data"
fi

if [[ "$*" == *"-c"* ]]; then
    echo "Timing the training process"
    startTalon=$(date +%s.%N)
fi


for i in `seq 0 1 10`; do
    echo "Starting client $i"
    sleep 1
    ../.venv/bin/python ../training.py $args &
done

endTalon=$(date +%s.%N)
runtimeTalon=$(python -c "print(${endTalon} - ${startTalon})")
echo "Training runtime: $runtimeTalon with args $args"

mkdir -p tmp/talon
mkdir -p tmp/speechcommands

if [[ "$*" == *"-t"* ]]; then
    mv ../../server/*.npz ./tmp/talon
    mv ./*.npz ./tmp/talon
else
    mv ../../server/*.npz ./tmp/speechcommands
    mv ./*.npz ./tmp/speechcommands
fi

# # # Enable CTRL+C to stop all background processes
# trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM
# wait
# Wait for all background processes to complete
echo "Stopping flwr server"

