#!/bin/bash

set -e
echo " Script running at $(pwd)"
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"/
mkdir -p tmp/talon
mkdir -p tmp/speechcommands

# Run the  script test.client.sh
# This will start the server and 10 clients
# run with default speechcommands data
startSC=$(date +%s.%N)
source test.client.sh -s
endSC=$(date +%s.%N)
runtimeSC=$(python -c "print(${endSC} - ${startSC})")

# start a timer to measure the time it takes to run the test
mv ../../server/*.npz tmp/speechcommands

# run with talon data
startTalon=$(date +%s.%N)
source test.client.sh -s -t
endTalon=$(date +%s.%N)
runtimeTalon=$(python -c "print(${endTalon} - ${startTalon})")

mv ../../server/*.npz tmp/talon

# compare the size of the files
scSize=0
for file in tmp/speechcommands/*.npz; do
    size=$(wc -c <"$file")
    scSize=$((scSize + size))
done
talonSize=0
for file in tmp/talon/*.npz; do
    size=$(wc -c <"$file")
    talonSize=$((talonSize + size))
done

echo "Speechcommands size: $scSize"
echo "Talon size: $talonSize"
echo "Speechcommands runtime: $runtimeSC"
echo "Talon runtime: $runtimeTalon"