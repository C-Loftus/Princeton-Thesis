import os

RECORDING_PATH = os.path.expanduser("~/.talon/recordings")
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_PATH, "data/talon-conversion")

parseCmd = lambda filename: filename.split("_")[0]

def parse():

# create training directory if it doesn't exist
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    for filename in os.listdir(RECORDING_PATH):

        cmd = parseCmd(filename)

        word_count = len(cmd.split(" "))

        if filename.endswith(".flac") and \
            word_count == 1 and \
            len([f for f in os.listdir(RECORDING_PATH) if parseCmd(f) == cmd]) > 1:

            command_path = os.path.join(OUTPUT_PATH, cmd)
            if not os.path.exists(command_path):
                os.makedirs(command_path)

            output_name = str(hash(filename) % 10000)

            # convert to wav
            os.system("ffmpeg -y -i %s/%s %s/%s.wav" %
                    (RECORDING_PATH, filename, command_path, output_name))
