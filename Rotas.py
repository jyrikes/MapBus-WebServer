from flask import Flask, request, jsonify
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from pydantic import BaseModel
import sqlite3

app = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Transportes UABJ')
spec.register(app)

class Localizacao(BaseModel):
    latitude: float
    longitude: float
    horario: str
    nome_ponto: str
    rota_id: int

def init_db():
    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Rotas (
        Rota_ID INTEGER PRIMARY KEY,
        Nome_Rota TEXT NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PosicoesUsuarios (
        ID INTEGER PRIMARY KEY,
        Latitude REAL,
        Longitude REAL,
        Horario TEXT,
        Nome_Ponto TEXT,
        Rota_ID INTEGER,
        FOREIGN KEY (Rota_ID) REFERENCES Rotas(Rota_ID)
    )
    ''')
    conn.close()

init_db()

def add_route(nome_rota):
    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Rotas (Nome_Rota) VALUES (?)", (nome_rota,))
    rota_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return rota_id

def add_point_to_route(rota_id, horario, latitude, longitude, nome_ponto):
    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO PosicoesUsuarios (Latitude, Longitude, Horario, Nome_Ponto, Rota_ID)
                      VALUES (?, ?, ?, ?, ?)''', (latitude, longitude, horario, nome_ponto, rota_id))
    conn.commit()
    conn.close()
@app.get('/server')
def mandarDados():
    try:
        conn = sqlite3.connect('banco_de_dados.db')
        query = "SELECT * FROM PosicoesUsuarios ORDER BY ID DESC LIMIT 1"
        result = pd.read_sql(query, conn)
        conn.close()

        if not result.empty:
            latest_location = Localizacao(
                latitude=result.iloc[0]['Latitude'],
                longitude=result.iloc[0]['Longitude'],
                horario=result.iloc[0]['Horario'],
                nome_ponto=result.iloc[0]['Nome_Ponto'],
                rota_id=result.iloc[0]['Rota_ID']
            )
            return latest_location.dict()
        else:
            return jsonify({"message": "No data available"}), 404

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.post('/server')
@spec.validate(
    body=Request(Localizacao), resp=Response(HTTP_201=Localizacao)
)
def receber_dados():
    body = request.context.body.dict()
    add_point_to_route(body['rota_id'], body['horario'], body['latitude'], body['longitude'], body['nome_ponto'])
    return jsonify(body), 201
if __name__ == '__main__':
    # Adicionar a rota "Rota 01 - Manhã (Ônibus)" e obter o ID
    rota_id = add_route("Rota 01 - Manhã (Ônibus)")

    # Adicionar pontos à rota
    pontos = [
        ("07:25", -8.343392, -36.421181, "Entrada da COHAB"),
        ("07:27", -8.344497, -36.413362, "Praça das Crianças"),
        ("07:30", -8.342243, -36.416842,"Escola Dr.Sebastião Cabral"),
        ("07:35", -8.337353, -36.419071,"Fórum")
        ("07:38", -8.333349, -36.417440,"Escola Prof.Donino")
        ("07:40", -8.331854, -36.413564,"Placa do Hospital Santa Fé")
        ("07:43", -8.326801, -36.405290,"UABJ")
        ("07:46", -8.319598, -36.39520,"AEB")
    ]
rota_id = add_route("Rota 03 - Manhã (Ônibus)")
pontos = [
]
    for ponto in pontos:
        horario, latitude, longitude, nome_ponto = ponto
        add_point_to_route(rota_id, horario, latitude, longitude, nome_ponto)
    
    app.run(debug=True)
﻿
