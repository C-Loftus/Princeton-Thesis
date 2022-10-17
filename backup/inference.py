import os

import requests
import torch
import torchaudio
import logging

torch.random.manual_seed(0)
SPEECH_URL = "https://pytorch-tutorial-assets.s3.amazonaws.com/VOiCES_devkit/source-16k/train/sp0307/Lab41-SRI-VOiCES-src-sp0307-ch127535-sg0042.wav"  # noqa: E501
SPEECH_FILE = "assets/speech.wav"

class GreedyCTCDecoder(torch.nn.Module):
    def __init__(self, labels, blank=0):
        super().__init__()
        self.labels = labels
        self.blank = blank

    def forward(self, emission: torch.Tensor) -> str:
        """Given a sequence emission over labels, get the best path string
        Args:
          emission (Tensor): Logit tensors. Shape `[num_seq, num_label]`.

        Returns:
          str: The resulting transcript
        """
        indices = torch.argmax(emission, dim=-1)  # [num_seq,]
        indices = torch.unique_consecutive(indices, dim=-1)
        indices = [i for i in indices if i != self.blank]
        return "".join([self.labels[i] for i in indices])

def logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("client.log"),
            logging.StreamHandler()
        ]
    )
    l = logging.getLogger(__name__)
    return l

def infer():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    l = logger(device)
    l.info(f"PyTorch version: {torch.__version__}")
    l.info(f"Torchaudio version: {torchaudio.__version__}")
    l.info(f"Device: {device}")

    if not os.path.exists(SPEECH_FILE):
        os.makedirs("assets", exist_ok=True)
        with open(SPEECH_FILE, "wb") as file:
            file.write(requests.get(SPEECH_URL).content)

    bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
    model = bundle.get_model().to(device)
    waveform, sample_rate = torchaudio.load(SPEECH_FILE)
    waveform = waveform.to(device)
    
    if sample_rate != bundle.sample_rate:
        waveform = torchaudio.functional.resample(waveform, sample_rate, bundle.sample_rate)

    with torch.inference_mode():
        features, _ = model.extract_features(waveform)

    with torch.inference_mode():
        emission, _ = model(waveform)

    decoder = GreedyCTCDecoder(labels=bundle.get_labels())

    transcript = decoder(emission[0])
    return transcript
