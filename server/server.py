from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
import uvicorn
import os, signal, dbm
import multiprocessing as mp

from federatedAlgo import start_flower

app = FastAPI()

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
    db['pid'] = 'Null PID'

# on startup, start the database
@app.on_event("startup")
async def startup_event():
    global db
    db = dbm.open('db', 'c')
    reset_db()

@app.on_event("shutdown")
async def shutdown_event():
    reset_db()
    db.close()

def isRunning():
    return db[b'server_running'] == b'1'

def get_connected_clients():
    return db.keys()

@app.get("/pid",  status_code=200)
async def get_pid():
    if isRunning():
        return {"detail": db.get("pid")}
    elif not isRunning():
        raise HTTPException(status_code=404, detail="Server not running")

@app.get("/start", status_code=200)
async def start_server(requiredClients : int = 2, strategy : str = 'FedAvg'):
    # check if server is already 
    if isRunning():
        raise HTTPException(status_code=404, detail="Server already running")
    elif not isRunning():
        p = mp.Process(target=start_flower, args=(requiredClients, strategy))
        p.start()
        db[b'pid'] = str(p.pid).encode('utf-8')
        db[b'server_running'] = b'1'
        return {"detail": "started"}

@app.get("/stop", status_code=200)
async def stop_server():
    if isRunning():
        pid = int(db[b'pid'])
        os.kill(pid, signal.SIGKILL)
        db[b'server_running'] = b'0'
        return {"detail": "stopped"}
    else:
        raise HTTPException(status_code=404, detail="Server not running")

@app.get("/running", status_code=200)
async def is_server_running():
    return {"detail": isRunning()}


if __name__ == "__main__":
    uvicorn.run("server:app", host="localhost", port=5000, debug=True, log_level="info")
