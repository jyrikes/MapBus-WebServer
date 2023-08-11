from flask import Flask, request, jsonify

from flask_pydantic_spec import FlaskPydanticSpec, Response, Request

from pydantic import BaseModel, Field

import sqlite3

app = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Transportes UABJ')
spec.register(app)



class Localizacao(BaseModel):
    latitude:int
    longitude:int


@app.post('/')
@spec.validate(
    body=Request(Localizacao), resp=Response(HTTP_201=Localizacao)
)
def receber_dados():
    try:
        
        body = request.context.body.dict() # Obtém os dados enviados pelo servidor Kotlin em formato JSON
        latitude = body['latitude']
        longitude = body['longitude']

        conn = sqlite3.connect('banco_de_dados.db')
        cursor = conn.cursor()


        # Insere os dados na tabela
        cursor.execute('''INSERT INTO PosicoesUsuarios (Latitude, Longitude) VALUES (?, ?)''',
                       (latitude, longitude))

        conn.commit()  # Salva as alterações no banco de dados
        conn.close()   # Fecha a conexão com o banco de dados

        return jsonify(body)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)