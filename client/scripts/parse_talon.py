import os, random, collections
import concurrent.futures
import requests,sys
import subprocess, random
import matplotlib.pyplot as plt
import numpy as np
 
RECORDING_PATH = os.path.expanduser("~/.talon/recordings")
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(SCRIPT_PATH, "../data")
HOSTNAME = os.uname()[1]
OUTPUT_PATH = os.path.join(SCRIPT_PATH, DATA_DIR, "talon-conversion")
USER_ID = hash(HOSTNAME)  % 10000
MIN_NUM_SAMPLES = 4
REMOTE_SERVER = "http://localhost:5000"
# settings = " -ar 16000 -b:a 256k -minrate 256k -maxrate 256k -y"
# settings = '-ss 0 -t 1 -f lavfi -i anullsrc=channel_layout=stereo -filter_complex
# "[1][0]concat=n=2:v=0:a=1[out]" -map "[out]" -c:a pcm_s16le'
#  Settings to  convert to 16 bit 16khz wav for training with torch
SETTINGS = ' -ss 0 -t 1 -af "apad=pad_len=1" -c:a pcm_s16le'

parseCmd = lambda filename: filename.split("-")[0]

def top30FromServer():
        # Send a web request to the server to get the list of commands
    result= requests.get(REMOTE_SERVER + "/commands")
    try:
        training_commands = result.json()['detail']
    except Exception as e:
        print(" Error getting commands from the server. Is the server running?")
        sys.exit(1)
    return training_commands

def validForTraining(filename, cmd) -> bool:
        
    words_in_command = len(cmd.split(" "))
    return filename.endswith(".flac") and \
            words_in_command == 1 and \
            len([f for f in os.listdir(RECORDING_PATH) if parseCmd(f) == cmd]) > MIN_NUM_SAMPLES

def makeCmdDir(cmd):
    command_path = os.path.join(OUTPUT_PATH, cmd)
    if not os.path.exists(command_path):
        os.makedirs(command_path)
    return command_path

def cleanupDir():
    # remove all folders in the output path
    for filename in os.listdir(OUTPUT_PATH):
        path = os.path.join(OUTPUT_PATH, filename)
        if os.path.isdir(path):
            for wav in os.listdir(path):
                os.remove(os.path.join(path, wav))
            print("Removing directory: ", path)
            os.rmdir(path)

    # remove all .txt files in the output path
    for filename in os.listdir(OUTPUT_PATH):
        path = os.path.join(OUTPUT_PATH, filename)
        if os.path.isfile(path) and path.endswith(".txt"):
            print("Removing file: ", path)
            os.remove(path)


def parse(getLabelsFromServer):

    wav_files = []
    commands = []
    timesSaid = {}

    def top30Locally():

        for filename in os.listdir(RECORDING_PATH):
            cmd = parseCmd(filename)
            if validForTraining(filename, cmd):
                timesSaid[cmd] = timesSaid.get(cmd, -1) + 1

        return dict(collections.Counter(timesSaid).most_common(30))

    top30Cmds = top30FromServer() if getLabelsFromServer else top30Locally()

    print("Top 30 commands: ", top30Cmds)

    for filename in os.listdir(RECORDING_PATH):

        cmdName = parseCmd(filename)

        if cmdName in top30Cmds:

            timesSaid[cmdName] = timesSaid.get(cmdName, -1) + 1
        
            command_path = makeCmdDir(cmdName)
    
            output_name = f'{USER_ID}_nohash_{timesSaid[cmdName]}.wav'

            commands.append(
             f'ffmpeg -i {RECORDING_PATH}/{filename} {SETTINGS} -y {command_path}/{output_name}'
            )

            full_path = os.path.join(OUTPUT_PATH, command_path, output_name)

            wav_files.append(str(full_path))

    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        print("Converting %d talon .flac recording files into the training format. This will use a lot of system resources." % len(commands))
        futures = [executor.submit(subprocess.run, cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for cmd in commands]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result.returncode != 0:
                print("Error converting file: %s" % result.stderr)
        print("Done converting talon recordings.")


        random.shuffle(wav_files)
        
        # Determine the split points
        train_split = int(0.8 * len(wav_files))
        val_split = train_split + int(0.1 * len(wav_files))
        
        # Split the file names
        train_filenames = wav_files[:train_split]
        val_filenames = wav_files[train_split:val_split]
        test_filenames = wav_files[val_split:]
        
        with open(os.path.join(OUTPUT_PATH, "training_list.txt"), "w") as f:    
            for filename in train_filenames:
                f.write(f'{filename}\n')

        with open(os.path.join(OUTPUT_PATH, "validation_list.txt"), "w") as f:    
            for filename in val_filenames:
                f.write(f'{filename}\n')
        with open(os.path.join(OUTPUT_PATH, "testing_list.txt"), "w") as f:    
            for filename in test_filenames:
                f.write(f'{filename}\n')
        print(commands[-1])



if __name__ == "__main__":
    getLabelsFromServer = sys.argv[1] == "-s" if len(sys.argv) > 1 else False
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    # clean up old data from previous runs
    cleanupDir()
    parse(getLabelsFromServer)