import flwr as fl

fl.server.start_server(config=fl.server.ServerConfig(num_rounds=3))