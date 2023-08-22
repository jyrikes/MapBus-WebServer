import requests
import json

BASE = "http://127.0.0.1:5000/"

data = {
    "Hora": "07:27",
    "Latitude": "-8.344497",
    "Longitude": "-36.413362",
    "local": "Praça das Crianças"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.get(BASE + "rota", json=data, headers=headers)
