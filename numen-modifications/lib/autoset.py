import os, multiprocessing, time
autoSet = {}

def update_scope():
    # Get the name of the current window and set a environment variable equal to true if it is focused

    def do_update():
        window_name = os.popen("xdotool getwindowfocus getwindowname").read()
        window_name = window_name.strip()
        os.environ[window_name] = "True"
        autoSet[window_name] = True 

        for key, _ in autoSet.items():
            if key != window_name:
                os.environ[key] = "False"
                autoSet[key] = False 

    while True:
        do_update()
        time.sleep(0.5)

if __name__ == "__main__":
    update_scope()
