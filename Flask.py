from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from Api import Api
import json
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from pydantic import BaseModel
import pandas as pd
from SQliteDB import SQliteDB as bd
import numpy as np
sqlite = bd('banco_de_dados.db')
app = Flask(__name__, template_folder='templates')
spec = FlaskPydanticSpec('flask', title='Transportes UABJ')
spec.register(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class Rota(BaseModel):
    latitude: float
    longitude: float
    horario: str
    nome_ponto: str
    rota_id: int

class Localizacao(BaseModel):
    latitude: float
    longitude: float
    horario: str
    rota_id: int

class Parada(BaseModel):
    horario: str
    nome_ponto: str
    rota_id: int

# Funções de login

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=40)], render_kw={"placeholder": "Nome de Usuário"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Senha"})
    submit = SubmitField("Registrar")

    def validate_username(self, field):
        existing_user_username = User.query.filter_by(
            username=field.data).first()
        if existing_user_username:
            raise ValidationError("Nome de usuário já existe")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=40)], render_kw={"placeholder": "Nome de Usuário"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Senha"})
    submit = SubmitField("Entrar")


# Rotas do site

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        api = Api("https://transporteuabj.pythonanywhere.com/server")
        data_from_api = api.get()
        return jsonify(data_from_api)  # Retorna os dados como JSON
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/transporte')
@login_required
def transporte():
    return render_template('transporte.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/mapa')
@login_required
def mapa():
    return render_template('mapa.html')


@app.route('/rotas', methods=['POST', 'GET'])
@login_required
def rotas():
    if request.method == 'POST':
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        horario = request.form.get('horario')
        nome_ponto = request.form.get('nome_ponto')
        rota_id = request.form.get('rota_id')

        rota = Rota(latitude=latitude, longitude=longitude,
                    horario=horario, nome_ponto=nome_ponto, rota_id=rota_id)
        apiRe = mandarRota()
        return apiRe
    else:
        return render_template('rotas.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# Servidor de longitude e latitude

@app.get('/user')
def mandarDados():
    try:


        latest_location = sqlite.get_latest_user_position()

        if latest_location:
            return latest_location
        else:
            return jsonify({"message": "No data available"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.post('/user')
@spec.validate(
    body=Request(Localizacao), resp=Response(HTTP_201=Localizacao)
)
def receber_dados():
    try:
        body = request.context.body.dict()
        latitude = body['latitude']
        longitude = body['longitude']
        horario = body['horario']
        rota_id = body['rota_id']

        sqlite.insert_user_position(latitude, longitude, horario, rota_id)

        return jsonify(body), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# Servidor de paradas

def haversine_vectorized(lat1, lon1, lat2_array, lon2_array):
    R = 6371.0  # Raio da Terra em quilômetros

    dlat = np.radians(lat2_array - lat1)
    dlon = np.radians(lon2_array - lon1)

    a = np.sin(dlat / 2) ** 2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2_array)) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    distancia = R * c
    return distancia

@app.get('/server')
def mandarRota():
  try:
        body = mandarDados()
        latitude = body['latitude']
        longitude = body['longitude']
        horario = body['horario']
        rota_id = body['rota_id']

        conectado = sqlite.connect()
        if conectado :
          conn = sqlite.conn
          query = 'SELECT Latitude, Longitude, Nome_Rota FROM Rotas'
          df = pd.read_sql_query(query, conn)

          latitudes = df['Latitude'].values
          longitudes = df['Longitude'].values

          df['distancia'] = haversine_vectorized(latitude, longitude, latitudes, longitudes)

          ponto_mais_proximo = df.loc[df['distancia'].idxmin()]

          conn.close()
          latest_parada = Parada(horario=horario, nome_ponto=ponto_mais_proximo["Nome_Rota"], rota_id=rota_id)
          return jsonify(latest_parada.dict()),200
  except Exception as e:
        return jsonify({"erro": str(e)}), 500
@app.post('/server')
def receberRota():
    try:
      # Obter os dados do formulário usando request.form
      latitude = request.form.get('latitude')
      longitude = request.form.get('longitude')
      horario = request.form.get('horario')
      nome_ponto = request.form.get('nome_ponto')
      rota_id = request.form.get('rota_id')
      sqlite.add_route(rota_id,horario,latitude,longitude,nome_ponto)
      # Criar um dicionário com os dados
      dados = {
          'Latitude': latitude,
          'Longitude': longitude,
          'Horario': horario,
          'Nome do Ponto': nome_ponto,
          'ID da Rota': rota_id
      }

      # Retornar uma resposta JSON usando jsonify
      return render_template("rotas.html")
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    
    

if __name__ == '__main__':
    sqlite.create_tables()
    app.run(debug=True)
