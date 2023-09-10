import sqlite3


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
                print(
                    f"Latitude: {latitude}, Longitude: {longitude}, Horário: {horario}, Rota ID: {rota_id}")
            else:
                print(f"Posição com ID {posicao_id} não encontrada.")
        except sqlite3.Error as error:
            print(f"Erro ao buscar posição: {error}")

    def __del__(self):
        # Fecha a conexão ao destruir a instância da classe
        self.cursor.close()
        self.connection.close()

    def inserir_parada(self, nomeDaRota, ponto):
        try:
            # Insere a posição na tabela "Rotas"
            sql_query = "INSERT INTO Rotas (Nome, Pontos) VALUES (?, ?)"
            data = (nomeDaRota, ponto)
            self.cursor.execute(sql_query, data)
            self.connection.commit()
            print("Rota do usuário inserida com sucesso!")
        except sqlite3.Error as error:
            print(f"Erro ao inserir rota do usuário: {error}")

    def get_parada(self, nomeDaRota):
        try:
            # Busca a posição do usuário pelo nome da rota
            sql_query = "SELECT Pontos FROM Rotas WHERE Nome = ?"
            data = (nomeDaRota,)
            self.cursor.execute(sql_query, data)
            posicao = self.cursor.fetchone()
            if posicao:
                # Retorna somente o valor da coluna "Pontos"
                return [nomeDaRota, posicao]
            else:
                print(f"Posição com ID {nomeDaRota} não encontrada.")
        except sqlite3.Error as error:
            print(f"Erro ao buscar rota do usuário: {error}")


# Criando a instância do banco de dados
