from flask import Flask, render_template, request, jsonify
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from pydantic import BaseModel, Field
import sqlite3
from datetime import datetime

app = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Transportes UABJ')
spec.register(app)

class Localizacao(BaseModel):
    latitude: int
    longitude: int
    Rota_ID: str

class PosicoesUsuarios(BaseModel):
    latitude: int
    longitude: int
    horario: datetime
    Rota_ID: str

@app.route('/', methods=['POST'])
@spec.validate(
    body=Request(Localizacao),
    resp=Response(HTTP_201=Localizacao)
)
def receber_dados():
    try:
        body = request.context.body.dict()
        latitude = body['latitude']
        longitude = body['longitude']
        Rota_ID = body['Rota_ID']
        
        horario = datetime.now()

        conn = sqlite3.connect('banco_de_dados.db')
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO PosicoesUsuarios (Latitude, Longitude, Horario, Rota_ID) 
                          VALUES (?, ?, ?, ?)''',
                       (latitude, longitude, horario, Rota_ID))

        conn.commit()
        conn.close()

        return jsonify(body), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/rota_page/<int:latitude>/<int:longitude>/<string:Rota_ID>')
def rota_page(latitude, longitude, Rota_ID):
    return render_template('rota.html', latitude=latitude, longitude=longitude, Rota_ID=Rota_ID)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)