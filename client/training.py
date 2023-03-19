# This file contains code from the link below that has been forked,changed and extended.
#  All referenced code is used fairly under a BSD License
# https://github.com/pytorch/tutorials/blob/master/intermediate_source/speech_command_classification_with_torchaudio_tutorial.py

import torch
import torch.nn.functional as F
import torch.optim as optim
import torchaudio
from collections import OrderedDict
import flwr as fl
from architecture import SubsetSC, M5

# Define all constants, datasets and hyper parameters for training
class TRAINING_CONFIG:
    def __init__(self, useTalon: bool = False):

        if useTalon:
            self.batch_size = 8
            self.n_epoch = 10
        else:
            self.batch_size = 256
            self.n_epoch = 2
        self.log_interval = 20  
        self.new_sample_rate = 8000
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.train_set = SubsetSC("training", useTalon=useTalon)
        self.test_set = SubsetSC("testing", useTalon=useTalon)

        waveform, sample_rate, label, speaker_id, utterance_number = self.train_set[0]

        self.labels = sorted(list(set(datapoint[2] for datapoint in self.train_set)))
        self.transform = torchaudio.transforms.Resample(
            orig_freq=sample_rate, new_freq=self.new_sample_rate
        )
        self.transformed = self.transform(waveform)

        if self.device == "cuda":
            self.num_workers = 1
            self.pin_memory = True
        else:
            self.num_workers = 0
            self.pin_memory = False

        self.train_loader = torch.utils.data.DataLoader(
            self.train_set,
            batch_size=self.batch_size,
            shuffle=True,
            collate_fn=collate_fn,
            num_workers=self.num_workers,
            pin_memory=self.pin_memory,
        )
        self.test_loader = torch.utils.data.DataLoader(
            self.test_set,
            batch_size=self.batch_size,
            shuffle=False,
            drop_last=False,
            collate_fn=collate_fn,
            num_workers=self.num_workers,
            pin_memory=self.pin_memory,
        )

        self.pbar_update = 1 / (len(self.train_loader) + len(self.test_loader))
        self.losses = []
        self.model = M5(
            n_input=self.transformed.shape[0],
            n_output=len(self.labels),
            useTalon=useTalon,
        )
        self.net = self.model.to(self.device)

        n = count_parameters(self.model)
        print(f"Number of parameters: {n}\n")
        print(f"Number of training examples: {len(self.train_set)}\n")
        print(f"Number of testing examples: {len(self.test_set)}\n")
        print(f"Number of classes: {len(self.labels)}\n")
        print(
            f"Length of training set: {len(self.train_loader)}, length of validation set: {len(self.test_loader)}\n"
        )
        print(f"Labels: {self.labels}\n")

        self.optimizer = optim.Adam(
            self.model.parameters(), lr=0.01, weight_decay=0.0001
        )
        self.scheduler = optim.lr_scheduler.StepLR(
            self.optimizer, step_size=20, gamma=0.1
        ) 
        # # The transform needs to live on the same device as the model and the data.
        self.transform = self.transform.to(self.device)


def number_of_correct(pred, target):
    # count number of correct predictions
    return pred.squeeze().eq(target).sum().item()


def get_likely_index(tensor):
    # find most likely label index for each element in the batch
    return tensor.argmax(dim=-1)


def index_to_label(index):
    # Return the word corresponding to the index in labels
    # This is the inverse of label_to_index
    return tc.labels[index]


def pad_sequence(batch):
    # Make all tensor in a batch the same length by padding with zeros
    batch = [item.t() for item in batch]
    batch = torch.nn.utils.rnn.pad_sequence(batch, batch_first=True, padding_value=0.0)
    return batch.permute(0, 2, 1)


def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def negative_log_tensor_reverse(tensor):
    # Return the negative log of the tensor
    return -tensor.log()

def adam_lr_scheduler(optimizer, epoch, lr):
    # Decay learning rate by a factor of 0.1 every 7 epochs
    if epoch % 7 == 0 and epoch:
        for param_group in optimizer.param_groups:
            param_group["lr"] *= 0.1
    return optimizer

def collate_fn(batch):
    def label_to_index(
        word,
    ):
        # Return the position of the word in labels
        return torch.tensor(tc.labels.index(word))

    tensors, targets = [], []

    for waveform, _, label, *_ in batch:
        tensors += [waveform]
        targets += [label_to_index(label)]

    # Group the list of tensors into a batched tensor
    tensors = pad_sequence(tensors)
    targets = torch.stack(targets)

    return tensors, targets


def train(model, epoch, log_interval):
    model.train()
    for batch_idx, (data, target) in enumerate(tc.train_loader):

        data = data.to(tc.device)
        target = target.to(tc.device)

        # apply transform and model on whole batch directly on device
        data = tc.transform(data)
        output = model(data)

        # negative log-likelihood for a tensor of size (batch x 1 x n_output)
        try:
            loss = F.nll_loss(output.squeeze(), target)
        except: # When we have a checkpoint and the model is not the same as the one we are trying to restore

            #  we need this try except block to manage restoring a model from a checkpoint
            try:
                if output.shape != target.shape:
                    target = target.expand(output.shape)
                loss = F.nll_loss(output.squeeze(), target)
            except: # Different error caused by different shapes now with 1 channel
                target = target.flatten()
                loss = F.nll_loss(output.squeeze(), target)

        tc.optimizer.zero_grad()
        loss.backward()
        tc.optimizer.step()

        # print training stats
        if batch_idx % log_interval == 0:
            print(
                f"Train Epoch: {epoch} [{batch_idx * len(data)}/{len(tc.train_loader.dataset)} ({100. * batch_idx / len(tc.train_loader):.0f}%)]\tLoss: {loss.item():.6f}"
            )

        # record loss and update the tc losses list
        tc.losses.append(loss.item())

def test(model, epoch):
    # set model to evaluation mode
    model.eval()
    correct = 0
    for data, target in tc.test_loader:

        data = data.to(tc.device)
        target = target.to(tc.device)

        # apply transform and model on whole batch directly on device
        data = tc.transform(data)
        output = model(data)

        pred = get_likely_index(output)
        correct += number_of_correct(pred, target)

    
    print(
        f"\nTest Epoch: {epoch}\tAccuracy: {correct}/{len(tc.test_loader.dataset)} ({100. * correct / len(tc.test_loader.dataset):.0f}%)\n"
    )
    #  special case for when we are restoring a model that was partially trained
    #  and has no losses recorded
    if len(tc.losses) == 0:
        loss = float(sum(tc.losses)) 
    else:
        loss = sum(tc.losses) / len(tc.losses) 
    accuracy = correct / len(tc.test_loader.dataset)
    return loss, accuracy


def predict(tensor):
    # Use the model to predict the label of the waveform
    tensor = tensor.to(tc.device)
    tensor = tc.transform(tensor)
    tensor = tc.model(tensor.unsqueeze(0))
    tensor = get_likely_index(tensor)
    tensor = index_to_label(tensor.squeeze())
    return tensor


class FlowerClient(fl.client.NumPyClient):
    def __init__(self, net, train_loader, test_loader) -> None:
        super().__init__()
        self.net = net
        self.train_loader = train_loader
        self.test_loader = test_loader

    def get_parameters(self, config):
        return [val.cpu().numpy() for _, val in self.net.state_dict().items()]

    def set_parameters(self, parameters, config=None):
        params_dict = zip(self.net.state_dict().keys(), parameters)
        state_dict = OrderedDict({k: torch.tensor(v) for k, v in params_dict})
        self.net.load_state_dict(state_dict, strict=True)

    def fit(self, parameters, config=None):
        self.set_parameters(parameters)
        EPOCH = 1
        LOG_INTERVAL = 100
        train(self.net, EPOCH, LOG_INTERVAL)
        return self.get_parameters(config={}), len(self.train_loader.dataset), {}

    def evaluate(self, parameters, config=None):
        self.set_parameters(parameters)
        loss, accuracy = test(self.net, self.test_loader)
        return loss, len(self.test_loader.dataset), {"accuracy": accuracy}


def main_training(useTalon=True):

    # global is fine since each client is a separate process and no state is updated
    # this training config makes functions cleaner with fewer hyperparams to pass
    global tc
    tc = TRAINING_CONFIG(useTalon)

    print("Starting flower client")
    # Start Flower client
    fl.client.start_numpy_client(
        server_address="127.0.0.1:8080",
        client=FlowerClient(tc.net, tc.train_loader, tc.test_loader),
    )
    print("Finished flower client")


if __name__ == "__main__":

    #  read the first argument in   
    import sys
    useTalon = False
    if len(sys.argv) > 1:
        useTalon = sys.argv[1] == "talon" or sys.argv[1] == "Talon" or sys.argv[1] == "-t" or sys.argv[1] == "--talon"
    print(f'Training with {"talon" if useTalon else "out talon, and instead using the default speech commands dataset."}')

    main_training(useTalon)

# DEBUG flwr 2023-03-15 17:39:41,287 | connection.py:38 | ChannelConnectivity.READY
#   File "<string>", line 1
    # print(1678916381.750501571 - )

    '''

    ouch', 'wipe']

Starting flower client
INFO flwr 2023-03-15 18:03:09,909 | grpc.py:50 | Opened insecure gRPC connection (no certificates were passed)
DEBUG flwr 2023-03-15 18:03:09,958 | connection.py:38 | ChannelConnectivity.IDLE
DEBUG flwr 2023-03-15 18:03:09,976 | connection.py:38 | ChannelConnectivity.READY
  File "<string>", line 1
    print(1678917790.731357867 - )
                                 ^
SyntaxError: invalid syntax
(federated speechcommands-py3.8) host@computer ~/P/thesis (master) [1]> Training with talon
Training with talon
n_input: 1, n_output: 30, stride: 8, n_channel: 64
Number of parameters: 96158

Number of training examples: 1888

Number of testing examples: 237

Number of classes: 30

Length of training set: 118, length of validation set: 15

'''