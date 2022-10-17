#!/usr/bin/bash
source ./.venv/bin/activate
python server/server.py & python client/main.py & python client/main.py

trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

# dirname "$(realpath $0)"