#!/bin/bash

set -e

mkdir -p tmp/talon
mkdir -p tmp/speechcommands

# Run the  script test.client.sh
# This will start the server and 10 clients

source test.client.sh -s

mv ../../server/*.npz tmp/