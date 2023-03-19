import flwr as fl, numpy as np
from flwr.common import Metrics
from typing import List, Tuple, Union, Optional, Dict
import sys
from flowerThread import StoppableThread, threading

ADDR = "127.0.0.1:8080"

# Code influenced by the following sources, used with permission and attribution:
# source: https://github.com/adap/flower/issues/487
# source: https://flower.dev/docs/save-progress.html

def fit_config(server_round: int) -> Dict[str, fl.common.Scalar]:
    config: Dict[str, fl.common.Scalar] = {
        "epoch_global": str(server_round),
        "epochs": str(1),
        "batch_size": str(32),
    }
    return config


def serverThread(userStrategy, clientManager, requiredClients):
    try:
        base_strategy_class = getattr(fl.server.strategy, userStrategy)
    except AttributeError:
        print(f'Strategy {userStrategy} not found. Returning...')


    class SaveModelStrategy(base_strategy_class):
        def aggregate_fit(
            self,
            server_round: int,
            results: List[Tuple[fl.server.client_proxy.ClientProxy, fl.common.FitRes]],
            failures: List[
                Union[
                    Tuple[fl.server.client_proxy.ClientProxy, fl.common.FitRes],
                    BaseException,
                ]
            ],
        ):
            weights = super().aggregate_fit(server_round, results, failures)
            if weights is not None:
                # Save weights
                print(f"Saving round {server_round} weights")
                np.savez(f"round-{server_round}-weights.npz", *weights)
            return weights


    # FedOpt, FedAdaGrad, FedAdam, FedYogi all require "initial_parameters to be set"
    strategy = SaveModelStrategy(
        # fraction_fit=1.0,
        min_fit_clients=requiredClients,
        min_available_clients=requiredClients,
        on_fit_config_fn=fit_config,
    )

    with open('server.log', 'w') as f:
        sys.stderr = f
        fl.server.start_server(
            server_address=ADDR,
            config=fl.server.ServerConfig(num_rounds=2),
            client_manager=clientManager,
            strategy=strategy
            # userStrategy(
                # evaluate_metrics_aggregation_fn=weighted_average),
        )


def start_flower(requiredClients: int, strategy: str)-> Tuple[fl.server.client_manager.ClientManager, threading.Thread]:
    # strategies = {
    #     "FedAvg": fl.server.strategy.FedAvg,
    #     "FedAvgM": fl.server.strategy.FedAvgM,
    #     "QFedAvg": fl.server.strategy.QFedAvg,
    #     "FaultTolerantFedAvg": fl.server.strategy.FaultTolerantFedAvg,
    #     "FedOpt": fl.server.strategy.FedOpt,
    #     "FedAdagrad": fl.server.strategy.FedAdagrad,
    #     "FedAdam": fl.server.strategy.FedAdam,
    #     "FedYogi": fl.server.strategy.FedYogi,
    # }
    # strategy = strategies[strategy]

    clientManager = fl.server.SimpleClientManager()

    handle = StoppableThread(target=serverThread, args=(strategy, clientManager, requiredClients))
    handle.start()

    return (clientManager, handle)

# Define metric aggregation function
def weighted_average(metrics: List[Tuple[int, Metrics]]) -> Metrics:
    # Multiply accuracy of each client by number of examples used
    accuracies = [num_examples * m["accuracy"] for num_examples, m in metrics]
    examples = [num_examples for num_examples, _ in metrics]

    # Aggregate and return custom metric (weighted average)
    return {"accuracy": sum(accuracies) / sum(examples)}
