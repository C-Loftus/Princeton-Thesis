In federated learning, the flower server needs to make a decision regarding how to aggregate the weights from the clients. Different aggregation strategies can be used to provide better properties for specialty tasks, or make up for technical limitations in the client system (power, network connection, processing power, etc).

When deciding to use a strategy, it is important to consider the following properties: [@https://doi.org/10.48550/arxiv.1602.05629]

- Non-IID: Any particular user's local data set will not necessarily be representative of the population distribution
- Unbalanced: The number of samples per user is not necessarily the same
- Massively Distributed: The number of users is very large
- Heterogeneous: The users' devices are different (e.g. different hardware, different operating systems, different software versions, etc.)
- Limited communication: The users' devices are not necessarily connected to the internet all the time, or have limited bandwidth

The most well known federated learning algorithm is FedAvg, this appeared in the same paper where the term "Federated Learning" was coined.[@https://doi.org/10.48550/arxiv.1602.05629] This algorithm works by randomly sampling from the users and averaging their update weights. However, this algorithm has some limitations. If we have particularly unbalanced data the algorithm may not synthesize between clients well. For this reason, the Federated Average with momentum algorithm was proposed. This strategy helps to eliminate the unbalanced data problem by using a momentum term to help the algorithm converge to a better solution. [@https://doi.org/10.48550/arxiv.1909.06335] This algorithm uses a gradient history to dampen oscillations during training. As a result, this algorithm also has the favorable property of being able to generally train more quickly than FedAvg.

While approaching training from perspective of data heterogeneity is one way to approach the tradeoff, we can also use strategies that try to limit network communication between the client and the server. One such strategy is known as QFedAvg. This strategy uses a quantization technique to reduce the amount of data that needs to be sent between the client and the server. [@https://doi.org/10.48550/arxiv.1602.05629] This strategy is particularly useful when the clients have limited network connectivity. If network speed is not the issue but rather interruptions in the connection, we can use FaultTolerantFedAvg.

Finally, we can also adapt the adaptive optimization methods of traditionally non-federated algorithms. We can use federated versions of adaptive optimizers, including Adagrad, Adam, and Yogi to make our systems easier to tune and gain more favorable convergence behavior. [@https://doi.org/10.48550/arxiv.2003.00295]

