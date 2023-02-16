import torch.nn.functional as F
import torchaudio,torch
import numpy as np
import sys ,os
new_path=os.path.join(os.getcwd(), 'client')
sys.path.append(new_path)
import architecture
import requests

REMOTE_SERVER = "http://localhost:5000"

class pretrainedModel(architecture.M5): 
    def __init__(self, n_input=1, n_output=35, stride=16, n_channel=32, useTalon=False):
        super().__init__(n_input, n_output, stride, n_channel, useTalon)
        self.load_weights('client/pretrained_weights.npy')
    
    def load_weights(self, weight_file):
        pretrained_weights = np.load(weight_file)
        model_weights = {}
        for name, param in self.named_parameters():
            if name in pretrained_weights:
                model_weights[name] = torch.from_numpy(pretrained_weights[name])
        self.load_state_dict(model_weights)

    def get_labels(self):
        result= REMOTE_SERVER + '/commands'
        try:
            training_commands = result.json()['detail']
        except Exception as e:
            print(" Error getting labels from the server. Is the server running?")
            sys.exit(1)
        self.labels = training_commands

    def get_likely_index(tensor):
        # find most likely label index for each element in the batch
        return tensor.argmax(dim=-1)


    def index_to_label(self,index):
        # Return the word corresponding to the index in labels
        # This is the inverse of label_to_index
        return self.labels[index]
 

    def predict(self,tensor):
        new_sample_rate = 8000
        transform = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=new_sample_rate)
        transformed = transform(waveform)

        # Use the model to predict the label of the waveform
        tensor = transform(tensor)
        tensor = model(tensor.unsqueeze(0))
        tensor = get_likely_index(tensor)
        tensor = index_to_label(tensor.squeeze())
        return tensor