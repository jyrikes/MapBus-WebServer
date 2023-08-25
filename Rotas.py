from flask import Flask, request, jsonify
import pandas as pd
import sqlite3
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from pydantic import BaseModel

app = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Transportes UABJ')
spec.register(app)

@app.route('/adicionar_ponto')
def adicionar_ponto():
    return render_template('rottasFile.html')

class Localizacao(BaseModel):
    latitude: float
    longitude: float
    horario: str
    nome_ponto: str
    rota_id: int


def init_db():
    with sqlite3.connect('banco_de_dados.db') as conn:
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


def add_route(nome_rota):
    with sqlite3.connect('banco_de_dados.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Rotas (Nome_Rota) VALUES (?)", (nome_rota,))
        return cursor.lastrowid


def add_point_to_route(rota_id, horario, latitude, longitude, nome_ponto):
    with sqlite3.connect('banco_de_dados.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO PosicoesUsuarios (Latitude, Longitude, Horario, Nome_Ponto, Rota_ID)
                          VALUES (?, ?, ?, ?, ?)''', (latitude, longitude, horario, nome_ponto, rota_id))


def init_app():
    init_db()

    # Rota 01 - Manhã (Ônibus)
    rota_id = add_route("Rota 01 - Manhã (Ônibus)")
    pontos = [
        ("07:25", -8.343392, -36.421181, "Entrada da COHAB"),
        ("07:27", -8.344497, -36.413362, "Praça das Crianças"),
        ("07:30", -8.342243, -36.416842, "Escola Dr.Sebastião Cabral"),
        ("07:35", -8.337353, -36.419071, "Fórum"),
        ("07:38", -8.333349, -36.417440, "Escola Prof.Donino"),
        ("07:40", -8.331854, -36.413564, "Placa do Hospital Santa Fé"),
        ("07:43", -8.326801, -36.405290, "UABJ"),
        ("07:46", -8.319598, -36.39520, "AEB")
    ]

    for ponto in pontos:
        horario, latitude, longitude, nome_ponto = ponto
        add_point_to_route(rota_id, horario, latitude, longitude, nome_ponto)

    # Rota 03 - Manhã (Ônibus)
    rota_id = add_route("Rota 03 - Manhã (Ônibus)")
    pontos = [
        ("09:00", -8.319598, -36.395205, "AEB"),
        ("09:02", -8.326801, -36.405290, "UABJ"),
        ("09:04", -8.343392, -36.421181, "ENTRADA DA COHAB"),
        ("09:08", -8.344497, -36.413362, "PRAÇA DAS CRIANÇAS"),
        ("09:10", -8.342243, -36.416842, "Escola DR. Sebastião Cabral"),
        ("09:15", -8.345663, -36.434173, "Trevo de Acesso"),
        ("09:18", -8.339146, -36.432410, "EREM João Monteiro"),
        ("09:20", -8.337285, -36.430412, "Posto PETROVIA"),
        ("09:22", -8.337575, -36.425721, "Centro"),
        ("09:24", -8.337353, -36.419071, "Fórum"),
        ("09:28", -8.328507, -36.420694, "Praça dos Eventos"),
        ("09:29", -8.325523, -36.418549, "Colégio Éxito"),
        ("09:32", -8.3213852,-36.4141771, "Praça do Maria Cristina"),
        ("09:37", -8.333349, -36.417440, "Escola Prof. Donino"),
        ("09:41", -8.331854, -36.413564, "Placa do Hospital Santa Fé"),
        ("09:43", -8.326801, -36.405290, "UABJ"),
        ("09:45", -8.319598, -36.395205, "AEB")
    ]

    for ponto in pontos:
        horario, latitude, longitude, nome_ponto = ponto
        add_point_to_route(rota_id, horario, latitude, longitude, nome_ponto)

    # Rota 01 - Tarde (Ônibus)
    rota_id = add_route("Rota 01 - Tarde (Ônibus)")
    pontos = [
        ("12:00", -8.319598, -36.395205, "AEB"),
        ("12:05", -8.326801, -36.405290, "UABJ"),
        ("12:10", -8.343392, -36.421181, "ENTRADA DA COHAB 1"),
        ("12:13", -8.344497, -36.413362, "PRAÇA DA CRIANÇA"),
        ("12:16", -8.342243, -36.416842, "ESCOLA DR.SEBATIÃO CABRAL"),
        ("12:20", -8.337353, -36.419071, "FÓRUM"),
        ("12:23", -8.333349, -36.417440, "ESCOLA PROF.DONINO"),
        ("12:25", -8.331854, -36.413564, "PLACA DE HOSPITAL SANTA FÉ"),
        ("12:28", -8.326801, -36.405290, "UABJ"),
        ("12:30", -8.319598, -36.395205, "AEB")
    ]

    for ponto in pontos:
        horario, latitude, longitude, nome_ponto = ponto
        add_point_to_route(rota_id, horario, latitude, longitude, nome_ponto)

    # Rota 03 - Tarde (Ônibus)
    rota_id = add_route("Rota 03 - Tarde (Ônibus)")
    pontos = [
        ("13:15", -8.319598, -36.395205, "AEB"),
        ("13:18", -8.326801, -36.405290, "UABJ"),
        ("13:22", -8.343392, -36.421181, "ENTRADA DA COHAB 1"),
        ("13:25", -8.344497, -36.413362, "PRAÇA DA CRIANÇA"),
        ("13:28", -8.342243, -36.416842, "ESCOLA DR.SEBATIÃO CABRAL"),
        ("13:32", -8.337353, -36.419071, "FÓRUM"),
        ("13:35", -8.333349, -36.417440, "ESCOLA PROF.DONINO"),
        ("13:38", -8.331854, -36.413564, "PLACA DE HOSPITAL SANTA FÉ"),
        ("13:41", -8.326801, -36.405290, "UABJ"),
        ("13:44", -8.319598, -36.395205, "AEB")
    ]

    for ponto in pontos:
        horario, latitude, longitude, nome_ponto = ponto
        add_point_to_route(rota_id, horario, latitude, longitude, nome_ponto)

    # Rota Final da Tarde (Ônibus)
    rota_id = add_route("Rota Final da Tarde (Ônibus)")
    pontos = [
        ("18:05", -8.319598, -36.395205, "AEB"),
        ("18:08", -8.326801, -36.405290, "UABJ"),
        ("18:13", -8.343392, -36.421181, "ENTRADA DA COHAB"),
        ("18:16", -8.344497, -36.413362, "PRAÇA DAS CRIANÇAS"),
        ("18:24", -8.342243, -36.416842, "Escola DR. Sebastião Cabral"),
        ("18:25", -8.345663, -36.434173, "Trevo de Acesso"),
        ("18:28", -8.339146, -36.432410, "EREM João Monteiro"),
        ("18:30", -8.337285, -36.430412, "Posto PETROVIA"),
        ("18:35", -8.337575, -36.425721, "Centro"),
        ("18:37", -8.337353, -36.419071, "Fórum"),
        ("18:42", -8.328507, -36.420694, "Praça dos Eventos"),
        ("18:44", -8.325523, -36.418549, "Colégio Éxito"),
        ("18:49", -8.3213852,-36.4141771, "Praça do Maria Cristina"),
        ("18:56", -8.333349, -36.417440, "Escola Prof. Donino"),
        ("18:58", -8.331854, -36.413564, "Placa do Hospital Santa Fé")
    ]

    for ponto in pontos:
        horario, latitude, longitude, nome_ponto = ponto
        add_point_to_route(rota_id, horario, latitude, longitude, nome_ponto)


@app.get('/server')
def mandarDados():
    try:
        with sqlite3.connect('banco_de_dados.db') as conn:
            query = "SELECT * FROM PosicoesUsuarios ORDER BY ID DESC LIMIT 1"
            result = pd.read_sql(query, conn)

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
@spec.validate(body=Request(Localizacao), resp=Response(HTTP_201=Localizacao))
def receber_dados():
    body = request.context.body.dict()
    add_point_to_route(body['rota_id'], body['horario'], body['latitude'], body['longitude'], body['nome_ponto'])
    return jsonify(body), 201


if __name__ == '__main__':
    init_app()
    app.run(debug=True)
