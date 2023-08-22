import requests
import json

BASE = "http://127.0.0.1:5000/"

data = {
    "latitude": -8.344497,
    "longitude": -36.413362,
    "Rota_ID": "4556867867"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(BASE, json=data, headers=headers)
print(response.json())

