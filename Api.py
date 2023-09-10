import requests as rq
from pydantic import BaseModel

class Rota(BaseModel):
    latitude: float
    longitude: float
    horario: str
    nome_ponto: str
    rota_id: int

class Api:
    def __init__(self, rota):
        self.rota = rota

    def get(self):
        response = rq.get(self.rota)
        response_dict = response.json() if response.status_code == 200 else {}
        return response_dict

    def post(self, rota: Rota):
        response = rq.post(self.rota, json=rota.dict())
        response_dict = response.json() if response.status_code == 200 else {}
        return response_dict


