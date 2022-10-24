from cgitb import reset
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn
import os, signal, dbm, sys, logging
import multiprocessing as mp
from typing import List, Tuple

import flwr as fl
from flwr.common import Metrics


# Define metric aggregation function
def weighted_average(metrics: List[Tuple[int, Metrics]]) -> Metrics:
    # Multiply accuracy of each client by number of examples used
    accuracies = [num_examples * m["accuracy"] for num_examples, m in metrics]
    examples = [num_examples for num_examples, _ in metrics]

    # Aggregate and return custom metric (weighted average)
    return {"accuracy": sum(accuracies) / sum(examples)}


# Define strategy
strategy = fl.server.strategy.FedAvg(
    evaluate_metrics_aggregation_fn=weighted_average)


app = FastAPI()

def reset_db():
    db[b'clients'] = b'0'
    db[b'server_running'] = b'0'
    db['pid'] = b'Null PID'

# on startup, start the database
@app.on_event("startup")
async def startup_event():
    global db
    db = dbm.open('db', 'c')
    reset_db()

# on shutdown, close the database and delete ephemeral files
@app.on_event("shutdown")
async def shutdown_event():
    reset_db()
    db.close()

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
def start_server():
    # redirect stdout to log file
    sys.stdout = open('server.log', 'w')
    sys.stderr = open('server.log', 'w')
    with open('server.log', 'w') as f:
        sys.stdout = f
        sys.stderr = f
        fl.server.start_server(
            server_address="0.0.0.0:8080",
            config=fl.server.ServerConfig(num_rounds=3),
            strategy=strategy,
        )

@app.get("/")
def read_root():
    return {"message": "World"}

def get_connected_clients():
    return db.keys()

@app.get("/pid")
async def get_pid():
    if db.get(b"server_running") == b'1':
        return {"message": db.get("pid")}
    return {'message': "Null PID"}

@app.get("/start")
async def start_server():
    # check if server is already 
    if db.get(b'server_running') == b'1':
        return {"message": "Server already running"}
    else:
        p = mp.Process(target=start_server)
        p.start()
        
        db[b'pid'] = str(p.pid).encode('utf-8')
        db[b'server_running'] = b'1'
        return {"message": "Server started"}

@app.get("/stop")
async def stop_server():
    if db.get(b'server_running') == b'1':
        pid = int(db[b'pid'])
        os.kill(pid, signal.SIGKILL)
        db[b'server_running'] = b'0'
        return {"message": "Server stopped"}
    else:
        return {"message": "Server not running"}


if __name__ == "__main__":
    uvicorn.run("server:app", host="localhost", port=5000, debug=True, log_level="info")
