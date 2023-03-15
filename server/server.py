from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
import uvicorn
import os
import shelve
import requests
from federatedAlgo import start_flower
from typing import List

app = FastAPI(openapi_url="/openapi.json")
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

default_commands = [
     "look",
      "map",
      "one",
      "gust",
      "bat",
      "quench",
      "vest",
      "trap",
      "sit",
      "zip",
      "three",
      "sun",
      "drum",
      "air",
      "whale",
      "yank",
      "near",
      "pit",
      "two",
      "end",
      "each",
      "odd",
      "harp",
      "crunch",
      "urge",
       "red",
      "plex",
      "fine",
      "jury",
      "home"
]


def reset_db():
    db['clients'] = '0'
    db['server_running'] = '0'

# on startup, start the database
@app.on_event("startup")
async def startup_event():
    global db
    db = shelve.open("db")
    reset_db()



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


@app.get("/")
async def root():
    return {"detail": "Successfully pinged server. Connect to API endpoints to interact with server."}

@app.get("/start", status_code=200)
async def start_server(clients: int = 4, strategy: str = 'FedAvgM'):
    # check if server is already
    if isRunning():
        raise HTTPException(status_code=404, detail="Server already running")
    elif not isRunning():
        global clientManager, serverHandle
        print(f'Starting server with {clients} clients and strategy {strategy}')
        clientManager, serverHandle = start_flower(clients, strategy)

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
async def host_ip():
    ip = requests.get('https://checkip.amazonaws.com').text.strip()
    # get port that fastapi is running on
    port = os.environ.get('PORT', 5000)
    ipAndPort = ip + ":" + str(port)
    return {"detail": ipAndPort}


@app.get("/flwr_ip")
async def get_ip():
    return {"detail": "127.0.0.1:8080"}

@app.get("/clients")
async def get_clients():
    if isRunning():
        return {"detail": len(clientManager)}
    else:
        raise HTTPException(status_code=404, detail="Server not running")

@app.get("/commands")
def command_list():
    if 'commands' in db: 
        return {
            "detail": db['commands']
        } 
    
    else:  
        return {
            "detail": default_commands
        }

@app.put("/commands")
def command_list(commands: List[str]):
    # Save the commands to the database
    db['commands'] = commands
    return 

if __name__ == "__main__":
    try:
        uvicorn.run("server:app", host="localhost",
                    port=5000, debug=True, log_level="info")
    except KeyboardInterrupt:
        import sys
        stop_server()
        sys.exit(0)
