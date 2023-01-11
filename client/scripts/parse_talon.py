import os
import concurrent.futures
import subprocess, random

RECORDING_PATH = os.path.expanduser("~/.talon/recordings")
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_PATH, "talon-conversion")

parseCmd = lambda filename: filename.split("-")[0]

def sufficientForTraining(filename, cmd) -> bool:
    words_in_command = len(cmd.split(" "))
    return filename.endswith(".flac") and \
            words_in_command == 1 and \
            len([f for f in os.listdir(RECORDING_PATH) if parseCmd(f) == cmd]) > 1

def makeCmdDir(cmd):
    command_path = os.path.join(OUTPUT_PATH, cmd)
    if not os.path.exists(command_path):
        os.makedirs(command_path)
    return command_path


def parse():
    # create training directory if it doesn't exist 
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    wav_files = []
    commands = []

    for filename in os.listdir(RECORDING_PATH):

        cmd = parseCmd(filename)

        if sufficientForTraining(filename, cmd):
        
            command_path = makeCmdDir(cmd)

            output_name = str(hash(filename) % 10000)

            commands.append("ffmpeg -y -i %s/%s %s/%s.wav" %
                (RECORDING_PATH, filename, command_path, output_name))

            full_path = os.path.join(OUTPUT_PATH, command_path, output_name + ".wav")

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
        
        with open(os.path.join(OUTPUT_PATH, "training_data.txt"), "w") as f:    
            for filename in train_filenames:
                f.write(f'{filename}\n')

        with open(os.path.join(OUTPUT_PATH, "validation_list.txt"), "w") as f:    
            for filename in val_filenames:
                f.write(f'{filename}\n')
        with open(os.path.join(OUTPUT_PATH, "testing_list.txt"), "w") as f:    
            for filename in test_filenames:
                f.write(f'{filename}\n')
        


if __name__ == "__main__":
    parse()