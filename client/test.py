import requests
# make a request to localhost:5000/start

url = "http://localhost:5000/openapi.json"
response = requests.get(url).json()
#  format it as json
response=(response['paths'])
for i in response:
    print(i)