from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import sqlite3



app = Flask(__name__, template_folder='templates')
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Nome de Usuário"})
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
        min=4, max=20)], render_kw={"placeholder": "Nome de Usuário"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Senha"})
    submit = SubmitField("Entrar")

class BancoDeDados:
    def __init__(self, database_name='banco_de_dados.db'):
        self.database_name = database_name
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def criar_tabelas(self):
        try:
            # Cria a tabela "Rotas"
            create_rotas_table_query = """
            CREATE TABLE IF NOT EXISTS Rotas (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome VARCHAR(100) NOT NULL,
                Pontos TEXT NOT NULL
            )
            """
            self.cursor.execute(create_rotas_table_query)

            # Cria a tabela "PosicoesUsuarios"
            create_posicoes_usuarios_table_query = """
            CREATE TABLE IF NOT EXISTS PosicoesUsuarios (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Latitude DECIMAL(10, 8) NOT NULL,
                Longitude DECIMAL(11, 8) NOT NULL,
                Horario DATETIME NOT NULL,
                Rota_ID INT NOT NULL,
                FOREIGN KEY (Rota_ID) REFERENCES Rotas(ID)
            )
            """
            self.cursor.execute(create_posicoes_usuarios_table_query)

            print("Tabelas criadas com sucesso!")
        except sqlite3.Error as error:
            print(f"Erro ao criar tabelas: {error}")

    def inserir_posicao(self, latitude, longitude, horario, rota_id):
        try:
            # Insere a posição na tabela "PosicoesUsuarios"
            sql_query = "INSERT INTO PosicoesUsuarios (Latitude, Longitude, Horario, Rota_ID) VALUES (?, ?, ?, ?)"
            data = (latitude, longitude, horario, rota_id)
            self.cursor.execute(sql_query, data)
            self.connection.commit()
            print("Posição do usuário inserida com sucesso!")
        except sqlite3.Error as error:
            print(f"Erro ao inserir posição do usuário: {error}")

    def get_posicao(self, posicao_id):
        try:
            # Busca a posição do usuário pelo ID
            sql_query = "SELECT Latitude, Longitude, Horario, Rota_ID FROM PosicoesUsuarios WHERE ID = ?"
            data = (posicao_id,)
            self.cursor.execute(sql_query, data)
            posicao = self.cursor.fetchone()
            if posicao:
                latitude, longitude, horario, rota_id = posicao
                print(f"Latitude: {latitude}, Longitude: {longitude}, Horário: {horario}, Rota ID: {rota_id}")
            else:
                print(f"Posição com ID {posicao_id} não encontrada.")
        except sqlite3.Error as error:
            print(f"Erro ao buscar posição: {error}")

    def __del__(self):
        # Fecha a conexão ao destruir a instância da classe
        self.cursor.close()
        self.connection.close()

@app.route('/')
@login_required
def home():
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


@app.route('/rotas')
@login_required
def rotas():
    banco = BancoDeDados()
    banco.criar_tabelas()
    
    # Exemplo de uso das funções
    latitude_usuario = -22.9083
    longitude_usuario = -43.1964
    horario_usuario = "2023-07-21 12:34:56"
    rota_id_usuario = 1
    
    banco.inserir_posicao(latitude_usuario, longitude_usuario, horario_usuario, rota_id_usuario )

    # Busca os dados da tabela "PosicoesUsuarios"
    banco.cursor.execute("SELECT * FROM PosicoesUsuarios")
    posicoes = banco.cursor.fetchall()

    banco.__del__()
    return render_template('rotas.html', posicoes=posicoes)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
    banco = BancoDeDados()
    banco.criar_tabelas()


    
    