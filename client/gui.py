import PySimpleGUIWeb as sg
import requests
sg.theme('DarkAmber')

import shelve

# Create a shelve object to store the server URL
global db
db = shelve.open("server.db")

# Create the layout of the GUI
layout = [ [sg.Text("Connect to a server for Federated Learning", font=("Helvetica", 22), justification='r')],
          [sg.Text(f'Saved Server URL: {db["url"] if "url" in db else "None"}', key="-URL-")],
          [sg.Text("Update Server URL:"), sg.Input()],
          [sg.Button("Connect"), sg.Button("Cancel")],
          [sg.Button("Check if the server is Running", key="-STATUS-")],
          [sg.Text("Response:", size=(15, 1)), sg.Multiline(size=(40, 10), key="-RESPONSE-")]]

# Create the window and show it
window = sg.Window("Server Connection", layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Close Window"):
        break
    if event == "Connect":
        # Send a GET request to the server and display the response
        url = values[0]
        db["url"] = url
        try:
            response = requests.get(url)
            window["-RESPONSE-"].update(response.text)
        except Exception as e:
            window["-RESPONSE-"].update(str(e))
        window["-URL-"].update(f'Saved Server URL: {db["url"] if "url" in db else "None"}')
        
    elif event == "-STATUS-":
        # Check if the server is running
        try:
            response = requests.get(db["url"])
            window["-RESPONSE-"].update(response.text)
        except Exception as e:
            window["-RESPONSE-"].update(str(e))

window.close()