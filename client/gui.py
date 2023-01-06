import PySimpleGUIWeb as sg
from training import main_training
import requests
sg.theme('DarkAmber')
import shelve
IP="http://localhost:8080"


global db
db = shelve.open("client.db")
db["url"] = "None" if "url" not in db else db["url"]

    
def create_ui():
    # Create a shelve object to store the server URL

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
        if event in (sg.WIN_CLOSED, "Close Window"):
            break
        if event == "-UPDATE-":
            url = values[0] if values[0] != "" else db["url"]
            db["url"] = url
            window["-URL-"].update(f'Saved Server URL: {db["url"] if "url" in db else "None"}')
            
        elif event == "-STATUS-":
            try:
                response = requests.get(db["url"])
            except requests.exceptions.ConnectionError as e:
                if "BadStatusLine" in str(e):
                    window["-RESPONSE-"].update("Server is running and ready for your training")
                else:
                    window["-RESPONSE-"].update("Server is not running")


        elif event == "-START-":
            # Start the server
            try:
                window["-RESPONSE-"].update("Starting the training process. This will take a while...")
                main_training()
                window["-RESPONSE-"].update("Finished training process")
            except Exception as e:
                window["-RESPONSE-"].update(str(e))


    window.close()

if __name__ == "__main__":
    create_ui()