import requests
import json

BASE = "http://127.0.0.1:5000/"

data = {
    "auto": "van",
    "ponto": "uabj"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.get(BASE + "rota", json=data, headers=headers)
print(response.text)