import torch
import torchaudio
import numpy as np
from torch import nn
import torch.nn.functional as F
import typer
import pyaudio
import wave

import requests
import sys
REMOTE_SERVER = "http://localhost:5000"

def top30FromServer():
        # Send a web request to the server to get the list of commands
    result= requests.get(REMOTE_SERVER + "/commands")
    try:
        training_commands = result.json()['detail']
    except Exception as e:
        print(" Error getting commands from the server. Is the server running?")
        sys.exit(1)
    return training_commands

def get_labels(fromServer=False):
    if fromServer:
        return top30FromServer()
    else: 
        return  [
        "backward", "bed", "bird", "cat", "dog", "down", "eight", "five", "follow", "forward",
        "four", "go", "happy", "house", "learn", "left", "marvin", "nine", "no", "off", "on",
        "one", "right", "seven", "sheila", "six", "stop", "three", "tree", "two", "up", "visual",
        "wow", "yes", "zero"
        ]

# Define the M5 model architecture
class M5(nn.Module):
    def __init__(self, n_input=1, n_output=35, stride=16, n_channel=32, useTalon=False):
        if useTalon:
            stride = 8
            n_channel = 64

        super().__init__()
        print(
            f"n_input: {n_input}, n_output: {n_output}, stride: {stride}, n_channel: {n_channel}"
        )
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

model = M5()

# Load the weights from the npz file
weights = np.load("MODEL", allow_pickle=True)

# Create a new state dict based on the reference state dict from the model
state_dict = model.state_dict()

# Update the state dict with the values from the npz file
for key in weights.keys():
    if key in state_dict:
        state_dict[key] = torch.from_numpy(weights[key])

# Load the state dict into the model
model.load_state_dict(state_dict)

def record_audio():

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1  # Set to 1 for mono recording
    RATE = 16000  # Set the sample rate to 16000 Hz
    RECORD_SECONDS = 1
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    print("Recording audio...")
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def main(record: bool = True, fromServer: bool = False):

    while True:
        record_audio() if record else print("Using sample audio file")

        filename = "output.wav" if record else "sample.wav.keep"

        waveform, sample_rate = torchaudio.load(filename)

        # Apply the same pre-processing steps as used in the training data
        # Here we know that the sample rate is 16000 Hz)
        mfcc_transform = torchaudio.transforms.MFCC(sample_rate=16000, n_mfcc=40)
        spectrogram_transform = torchaudio.transforms.Spectrogram(n_fft=1024, hop_length=512)

        mfcc = mfcc_transform(waveform)
        spectrogram = spectrogram_transform(waveform)

        # Combine the MFCC and spectrogram into a single input tensor
        input_tensor = torch.cat([mfcc, spectrogram], dim=0)

        # Add a batch dimension
        input_tensor = input_tensor.unsqueeze(0)

        # Pass the input tensor through the model
        model.eval()
        output = model(input_tensor)


        # Convert the output to a probability distribution
        probabilities = torch.softmax(output, dim=1)

        labels = get_labels(fromServer)        

        predicted_label = labels[probabilities.argmax()]

        print("The predicted label is:\n", predicted_label)


if __name__ == "__main__":
    main()