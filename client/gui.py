# references:  https://github.com/PySimpleGUI/PySimpleGUI/issues/276

import threading
import PySimpleGUIWeb as sg
from training import main_training
from scripts.parse_talon import parse
import requests,os 
from contextlib import redirect_stdout
from image import gif 
gif103 = gif().gif103

import shelve
sg.theme('DarkAmber')
IP="http://localhost:8080"
RECORDING_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/talon-conversion")


global db
db = shelve.open("client.db")
db["url"] = "None" if "url" not in db else db["url"]
db["training"] = False


def start_loading(window):
    window.Element('_IMAGE_').update(data= gif103)
    
def stop_loading(window):
    window.Element('_IMAGE_').update(data= None)

def valid_talon_data():

    def directory_exists():
        os.path.exists(RECORDING_PATH) and os.path.isdir(RECORDING_PATH)

    def has_training_data():
        for root, dirs, files in os.walk(RECORDING_PATH):
            for file in files:
                if file.endswith(".wav"):
                    return True
        return False

    def has_split_lists():
        # Check that training_list.txt exists   
        return os.path.exists(os.path.join(RECORDING_PATH, "training_list.txt")) and \
            os.path.exists(os.path.join(RECORDING_PATH, "validation_list.txt")) and \
            os.path.exists(os.path.join(RECORDING_PATH, "testing_list.txt"))
    
    return directory_exists() and has_training_data() and has_split_lists()

def training_manager(window):
    window["-RESPONSE-"].update("Starting the training process. This will take a while...")
    db["training"] = True
    main_training(useTalon=valid_talon_data())
    db["training"] = False
    window["-RESPONSE-"].update("Finished training process")

def create_ui():

    # Create the layout of the GUI
    layout = [[sg.Text("Connect to a server for Federated Learning", font=("Helvetica", 22), justification='r')],
            [sg.Text(f'Saved Server URL: {db["url"] if "url" in db else "None"}', key="-URL-")],
            [sg.Text("Update Server URL:"), sg.Input(), sg.Button("Update", key="-UPDATE-")], 
            [sg.Button("Ping Server", key="-STATUS-")],
            [sg.Button("Start Federated Training on Your Data", key="-START-")],
            [sg.Button("Convert Talon Data", key="-CONVERT-")],
            [sg.Image(data=None, key='_IMAGE_')],
            [sg.Text("Response:", size=(15, 1)), sg.Multiline(size=(40, 10), key="-RESPONSE-")]]

    window = sg.Window("Connection", layout)
    handle = threading.Thread(target=training_manager, args=(window,))

    def check_if_finished(handle):
        if not handle.is_alive():
            window["-RESPONSE-"].update("Finished training process")
            db["training"] = False

    while True:
        if db["training"]:
            window["-START-"].update("Stop Federated Training Process")

        event, values = window.read()

        if event and db["training"]:
            window["-RESPONSE-"].update("Training in progress. Please wait until it is finished.")
            continue

        elif event in (sg.WIN_CLOSED, "Close Window"):
            break
        elif event == "-UPDATE-":
            url = values[0] if values[0] != "" else db["url"]
            db["url"] = url
            window["-URL-"].update(f'Saved Server URL: {db["url"] if "url" in db else "None"}')
            
        elif event == "-STATUS-":
            msg = None
            try:
                msg = requests.get(db["url"])
            # we are expecting an error since we aren't connecting with the flower client.
            # we just want to make sure the server is running and ready for our training
            except requests.exceptions.ConnectionError as e:
                if "BadStatusLine" in str(e):
                    msg = "Server is running and ready for your training"
            finally:
                window["-RESPONSE-"].update(msg)

        elif event == "-START-" and db["training"] == False:
            try:
                handle.start()
                # runs in the background
                check_if_finished(handle)
                start_loading(window)
                msg = f'Running training process on {db["url"]} {"without" if not valid_talon_data() else "with"} Talon data'
            except Exception as e:
                window["-RESPONSE-"].update(str(e))
        elif event == "-START-" and db["training"] == True:
            window["-RESPONSE-"].update("Training in progress. Please wait until it is finished.")

        elif event == "-CONVERT-":
            try:
                with open("convert.log", "w") as f:
                    with redirect_stdout(f):
                        window["-RESPONSE-"].update("Converting Talon data. This may take a while and use a lot of resources...")
                        start_loading(window)
                        parse(getLabelsFromServer=True)
                        stop_loading(window)
                window["-RESPONSE-"].update("Successfully converted Talon data")
            except Exception as e:
                window["-RESPONSE-"].update(str(e))



    window.close()

if __name__ == "__main__":
    create_ui()



