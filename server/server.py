from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn
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

SERVER_RUNNING = False

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/start_server")
async def start_server():
    # check if server is already 
    if SERVER_RUNNING:
        return {"message": "Server already running"}
    else:
        SERVER_RUNNING = True
        def start_server():
            fl.server.start_server(
                server_address="0.0.0.0:8080",
                config=fl.server.ServerConfig(num_rounds=3),
                strategy=strategy,
            )
        p = mp.Process(target=start_server)
        p.start()
        return {"message": "Server started"}

@app.get("/stop_server")
async def stop_server():
    if SERVER_RUNNING:
        SERVER_RUNNING = False
        fl.server.
        return {"message": "Server stopped"}
    else:
        return {"message": "Server not running"}


@app.get('/profile')
def my_profile():
    response_body = {
        "name": "Colton",
        "about" :"Hello! I'm a full stack developer that loves python and javascript"
    }

    return response_body


if __name__ == "__main__":
    uvicorn.run("server:app", host="localhost", port=5000, debug=True, log_level="info")
