# This file contains code from the link below that has been forked,changed and extended. 
#  All referenced code is use under a BSD License
# https://github.com/pytorch/tutorials/blob/master/intermediate_source/speech_command_classification_with_torchaudio_tutorial.py

import os
from torchaudio.datasets import SPEECHCOMMANDS
from torch import nn
import torch.nn.functional as F


class M5(nn.Module):
    def __init__(self, n_input=1, n_output=35, stride=16, n_channel=32, useTalon=False):
        if useTalon:
            stride=8
            n_channel=64

        super().__init__()
        print(f"n_input: {n_input}, n_output: {n_output}, stride: {stride}, n_channel: {n_channel}")
        self.conv1 = nn.Conv1d(n_input, n_channel, kernel_size=80, stride=stride)
        self.bn1 = nn.BatchNorm1d(n_channel)
        self.pool1 = nn.MaxPool1d(4)
        self.conv2 = nn.Conv1d(n_channel, n_channel, kernel_size=3)
        self.bn2 = nn.BatchNorm1d(n_channel)
        self.pool2 = nn.MaxPool1d(4)
        self.conv3 = nn.Conv1d(n_channel, 2 * n_channel, kernel_size=3)
        self.bn3 = nn.BatchNorm1d(2 * n_channel)
        self.pool3 = nn.MaxPool1d(4)
        self.conv4 = nn.Conv1d(2 * n_channel, 2 * n_channel, kernel_size=3)
        self.bn4 = nn.BatchNorm1d(2 * n_channel)
        self.pool4 = nn.MaxPool1d(4)
        self.fc1 = nn.Linear(2 * n_channel, n_output) 

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(self.bn1(x))
        x = self.pool1(x)
        x = self.conv2(x)
        x = F.relu(self.bn2(x))
        x = self.pool2(x)
        x = self.conv3(x)
        x = F.relu(self.bn3(x))
        x = self.pool3(x)
        x = self.conv4(x)
        x = F.relu(self.bn4(x))
        x = self.pool4(x)
        x = F.avg_pool1d(x, x.shape[-1])
        x = x.permute(0, 2, 1)
        x = self.fc1(x)
        return F.log_softmax(x, dim=2)

    # def forward(self, x):
    #     # Do the same thing as above but  print the output shape at each layer            
    #     print(f"input shape: {x.shape}")
    #     x = self.conv1(x)
    #     print(f"conv1 shape: {x.shape}")
    #     x = F.relu(self.bn1(x))
    #     print(f"bn1 shape: {x.shape}")
    #     x = self.pool1(x)
    #     print(f"pool1 shape: {x.shape}")
    #     x = self.conv2(x)
    #     print(f"conv2 shape: {x.shape}")
    #     x = F.relu(self.bn2(x))
    #     print(f"bn2 shape: {x.shape}")
    #     x = self.pool2(x)
    #     print(f"pool2 shape: {x.shape}")
    #     x = self.conv3(x)
    #     print(f"conv3 shape: {x.shape}")
    #     x = F.relu(self.bn3(x))
    #     print(f"bn3 shape: {x.shape}")
    #     x = self.pool3(x)
    #     print(f"pool3 shape: {x.shape}")
    #     x = self.conv4(x)
    #     print(f"conv4 shape: {x.shape}")
    #     x = F.relu(self.bn4(x))
    #     print(f"bn4 shape: {x.shape}")
    #     x = self.pool4(x)
    #     print(f"pool4 shape: {x.shape}")
    #     x = F.avg_pool1d(x, x.shape[-1])
    #     print(f"avg_pool1d shape: {x.shape}")
    #     x = x.permute(0, 2, 1)
    #     print(f"permute shape: {x.shape}")
    #     x = self.fc1(x)
    #     print(f"fc1 shape: {x.shape}")
    #     return F.log_softmax(x, dim=2)


class SubsetSC(SPEECHCOMMANDS):
    def __init__(self, subset: str = None, downloadDataset: bool = True, useTalon: bool = False):
        root_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
        super().__init__(root_dir, download= downloadDataset)

        def load_list(filename):
            if useTalon:
                # generate relative path from string
                filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
                filepath = os.path.join(filepath, "talon-conversion")
                filepath = os.path.join(filepath, filename)

            else:
                filepath = os.path.join(self._path, filename)
            with open(filepath) as fileobj:
                return [os.path.normpath(os.path.join(self._path, line.strip())) for line in fileobj]

        if subset == "validation":
            self._walker = load_list("validation_list.txt")
        elif subset == "testing":
            self._walker = load_list("testing_list.txt")
         # the speech commands data set does not have an explicit training list
        elif subset == "training" and not useTalon:
            excludes = load_list("validation_list.txt") + load_list("testing_list.txt")
            excludes = set(excludes)
            self._walker = [w for w in self._walker if w not in excludes]
        # If we are using the talon data set there's an explicit training list
        elif subset == "training" and useTalon:
            self._walker = load_list("training_list.txt")

if __name__ == "__main__":
     # print the full path of this script
    print(os.path.realpath(__file__))
    sc = SubsetSC(subset="training", downloadDataset=False, useTalon=True)