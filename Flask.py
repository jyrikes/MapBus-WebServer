from flask import Flask, render_template, url_for, redirect
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import BancoDeDados as bd

app = Flask(__name__, template_folder='templates')
api = Api(app)
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

class HelloWorld(Resource):
    def get(self, auto, ponto):
        return {"auto": auto, "ponto": ponto}

api.add_resource(HelloWorld, "/helloworld/<string:auto>/<string:ponto>")    

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
    banco = bd.BancoDeDados()
    banco.criar_tabelas()

    # Busca os dados da tabela "PosicoesUsuarios"
    banco.cursor.execute("SELECT * FROM PosicoesUsuarios")
    posicoes = banco.cursor.fetchall()

    # Busca os dados da tabela "Rotas"
    rota1 = banco.get_parada('Rota da manhã')
    print(rota1)

    # Função para determinar o turno com base no horário
    def posicao_turno(horario):
        if horario is not None:
            if horario.split()[1] < '12:00:00':
                return 'manha'
            elif horario.split()[1] < '18:00:00':
                return 'tarde'
            else:
                return 'noite'
        return None

    # Coloque aqui a variável que armazena o turno selecionado (manha, tarde, noite)
    # Por exemplo, você pode mudar para 'tarde' ou 'noite' conforme a seleção do usuário
    selected_content = 'manha'

    banco.__del__()
    return render_template('rotas.html', posicoes=posicoes, rota1=rota1, posicao_turno=posicao_turno, selected_content=selected_content)


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


if __name__ == '__main__':
    app.run(debug=True)
    banco = bd.BancoDeDados()
    banco.criar_tabelas()
