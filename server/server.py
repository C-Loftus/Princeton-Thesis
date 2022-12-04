from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
import uvicorn
import os
import signal
import shelve
import requests
from federatedAlgo import start_flower
import flwr as fl
from multiprocessing import Queue

app = FastAPI()
clientManager = None
serverHandle = None

origins = [
    "http://localhost:5000",
    "localhost:5000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def reset_db():
    db['clients'] = '0'
    db['server_running'] = '0'

# on startup, start the database


@app.on_event("startup")
async def startup_event():
    global db
    db = shelve.open("db")
    reset_db()


@app.on_event("shutdown")
async def shutdown_event():
    reset_db()
    db.close()


def isRunning():
    return db['server_running'] == '1'


def get_connected_clients():
    return db.keys()

# @app.get("/pid",  status_code=200)
# async def get_pid():
#     if isRunning():
#         return {"detail": db.get("pid")}
#     elif not isRunning():
#         raise HTTPException(status_code=404, detail="Server not running")


@app.get("/start", status_code=200)
async def start_server(requiredClients: int = 2, strategy: str = 'FedAvg'):
    # check if server is already
    if isRunning():
        raise HTTPException(status_code=404, detail="Server already running")
    elif not isRunning():
        global clientManager, serverHandle
        clientManager, serverHandle = start_flower(requiredClients, strategy)

        db['server_running'] = '1'

        return {"detail": "started"}


@app.get("/stop", status_code=200)
async def stop_server():
    if isRunning():

        db['server_running'] = '0'
        return {"detail": "stopped"}
    else:
        raise HTTPException(status_code=404, detail="Server not running")


@app.get("/running", status_code=200)
async def is_server_running():
    return {"detail": isRunning()}


@app.get("/host_ip")
async def get_ip():
    ip = requests.get('https://checkip.amazonaws.com').text.strip()
    # get port that fastapi is running on
    port = os.environ.get('PORT', 5000)
    ipAndPort = ip + ":" + str(port)
    return {"detail": ipAndPort}


@app.get("/ip")
async def get_ip():
    return {"detail": "127.0.0.1:8080"}


@app.get("/clients")
async def get_clients():
    if isRunning():
        return {"detail": len(clientManager)}
    else:
        raise HTTPException(status_code=404, detail="Server not running")


if __name__ == "__main__":
    try:
        uvicorn.run("server:app", host="localhost",
                    port=5000, debug=True, log_level="info")
    except KeyboardInterrupt:
        import sys
        sys.exit(0)
