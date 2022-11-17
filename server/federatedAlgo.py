import flwr as fl
from flwr.common import Metrics
from typing import List, Tuple
import sys

ADDR = "0.0.0.0:8080"

def start_flower(requiredClients: int, strategy: str):
    strategies = {
        "FedAvg": fl.server.strategy.FedAvg,
        "FedAvgM": fl.server.strategy.FedAvgM,
        "QFedAvg": fl.server.strategy.QFedAvg,
        "FaultTolerantFedAvg": fl.server.strategy.FaultTolerantFedAvg,
        "FedOpt": fl.server.strategy.FedOpt,
        "FedAdagrad": fl.server.strategy.FedAdagrad,
        "FedAdam": fl.server.strategy.FedAdam,
        "FedYogi": fl.server.strategy.FedYogi,
    }
    userStrategy = strategies[strategy]
    # redirect stdout to log file
    sys.stdout = open('server.log', 'w')
    with open('server.log', 'w') as f:
        sys.stderr = f
        fl.server.start_server(
            server_address= ADDR,
            config=fl.server.ServerConfig(num_rounds=3),
            strategy=userStrategy(
            evaluate_metrics_aggregation_fn=weighted_average),
        )

# Define metric aggregation function
def weighted_average(metrics: List[Tuple[int, Metrics]]) -> Metrics:
    # Multiply accuracy of each client by number of examples used
    accuracies = [num_examples * m["accuracy"] for num_examples, m in metrics]
    examples = [num_examples for num_examples, _ in metrics]

    # Aggregate and return custom metric (weighted average)
    return {"accuracy": sum(accuracies) / sum(examples)}


