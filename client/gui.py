import threading
import PySimpleGUIWeb as sg
from training import main_training
import requests
from contextlib import redirect_stdout
import io

sg.theme('DarkAmber')
import shelve
IP="http://localhost:8080"


global db
db = shelve.open("client.db")
db["url"] = "None" if "url" not in db else db["url"]
db["training"] = False


def training_manager(window):
    window["-RESPONSE-"].update("Starting the training process. This will take a while...")
    db["training"] = True
    main_training()
    db["training"] = False
    window["-RESPONSE-"].update("Finished training process")

def create_ui():

    # Create the layout of the GUI
    layout = [[sg.Text("Connect to a server for Federated Learning", font=("Helvetica", 22), justification='r')],
            [sg.Text(f'Saved Server URL: {db["url"] if "url" in db else "None"}', key="-URL-")],
            [sg.Text("Update Server URL:"), sg.Input(), sg.Button("Update", key="-UPDATE-")], 
            [sg.Button("Ping Server", key="-STATUS-")],
            [sg.Button("Start Federated Training Process", key="-START-")],
            [sg.Button("Stop Federation Training Process", key="-STOP-")],
            [sg.Button("Convert Talon Data", key="-CONVERT-")],
            [sg.Text("Response:", size=(15, 1)), sg.Multiline(size=(40, 10), key="-RESPONSE-")]]

    window = sg.Window("Connection", layout)

    while True:
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

        elif event == "-START-":
            try:
                handle = threading.Thread(target=training_manager, args=(window,))
                handle.start()
            except Exception as e:
                window["-RESPONSE-"].update(str(e))

    window.close()

if __name__ == "__main__":
    create_ui()