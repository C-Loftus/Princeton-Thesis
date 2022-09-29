#!/usr/bin/bash
source ./.venv/bin/activate
python client/server.py & python client/client.py & python client/client.py

trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT