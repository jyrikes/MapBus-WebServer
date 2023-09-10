import sqlite3
import json 

class SQliteDB:
    def __init__(self, db_name):
        self.db_name = db_name

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {str(e)}")
            return False
    

    def close(self):
        try:
            if self.conn:
                self.conn.close()
        except Exception as e:
            print(f"Erro ao fechar a conexão com o banco de dados: {str(e)}")

    def create_tables(self):
        try:
            if self.connect():
                # Crie aqui as tabelas do seu banco de dados SQLite
                self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Rotas (
                        Rota_ID INTEGER PRIMARY KEY,
                        Nome_Rota TEXT NOT NULL,
                        Latitude REAL,
                        Longitude REAL,
                        Horario TEXT,
                        id_rota INTEGER
                    )
                ''')
                self.cursor.execute('''
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
                self.conn.commit()
        except Exception as e:
            print(f"Erro ao criar tabelas no banco de dados: {str(e)}")
        finally:
            self.close()

    def add_route(self, rota_id, horario, latitude, longitude, nome_ponto):
        try:
            if self.connect():
                self.cursor.execute("INSERT INTO Rotas (Nome_Rota,Latitude,Longitude,Horario,id_rota) VALUES (?,?,?,?,?)", (nome_ponto, latitude,longitude,horario,rota_id))
                self.conn.commit()
                return self.cursor.lastrowid
        except Exception as e:
            print(f"Erro ao adicionar rota no banco de dados: {str(e)}")
        finally:
            self.close()

    def add_point_to_route(self, rota_id, horario, latitude, longitude, nome_ponto):
        try:
            if self.connect():
                self.cursor.execute('''INSERT INTO PosicoesUsuarios (Latitude, Longitude, Horario, Nome_Ponto, Rota_ID)
                                      VALUES (?, ?, ?, ?, ?)''', (latitude, longitude, horario, nome_ponto, rota_id))
                self.conn.commit()
        except Exception as e:
            print(f"Erro ao adicionar ponto à rota no banco de dados: {str(e)}")
        finally:
            self.close()


    def init_app(self, json_data):
        # Carregue os dados da string JSON
        data = json.loads(json_data)

        for rota_data in data['rotas']:
            rota_nome = rota_data['nome']
              # Adicione a rota e obtenha o ID da rota

            for ponto_data in rota_data['pontos']:
                rota_id = ponto_data['id_rota']
                horario = ponto_data['horario']
                latitude = ponto_data['latitude']
                longitude = ponto_data['longitude']
                nome_ponto = ponto_data['nome_ponto']

                # Adicione cada ponto à rota usando a função add_point_to_route
                self.add_route(rota_id, horario, latitude, longitude, nome_ponto)
                
    def insert_user_position(self, latitude, longitude, horario, rota_id):
        try:
            if self.connect():
                self.cursor.execute('''INSERT INTO PosicoesUsuarios (Latitude, Longitude, Horario, Rota_ID)
                                      VALUES (?, ?, ?, ?)''', (latitude, longitude, horario, rota_id))
                self.conn.commit()
        except Exception as e:
            print(f"Erro ao inserir posição do usuário no banco de dados: {str(e)}")
        finally:
            self.close()
            
    def get_latest_user_position(self):
        try:
            if self.connect():
                query = '''
                    SELECT Latitude, Longitude, Horario, Rota_ID
                    FROM PosicoesUsuarios
                    ORDER BY ID DESC
                    LIMIT 1
                '''
                self.cursor.execute(query)
                result = self.cursor.fetchone()
                if result:
                    latitude, longitude, horario, rota_id = result
                    return {
                        "latitude": latitude,
                        "longitude": longitude,
                        "horario": horario,
                        "rota_id": rota_id
                    }
                else:
                    return None
        except Exception as e:
            print(f"Erro ao obter a posição do usuário mais recente do banco de dados: {str(e)}")
            return None
        finally:
            self.close()