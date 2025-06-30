import sqlite3
import unicodedata

class SistemaDeCadastro:
    def __init__(self, db_name='estudantes.db'):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS estudantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                telefone TEXT NOT NULL,
                sexo TEXT NOT NULL,
                data_nascimento TEXT NOT NULL,
                endereco TEXT NOT NULL,
                curso TEXT NOT NULL,
                picture BLOB NOT NULL
            )
        ''')

        self.c.execute('''
            CREATE TABLE IF NOT EXISTS cursos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE
            )
        ''')

        cursos_iniciais = ['Outros']
        for curso in cursos_iniciais:
            try:
                self.c.execute("INSERT INTO cursos (nome) VALUES (?)", (curso,))
            except sqlite3.IntegrityError:
                pass

        self.conn.commit()

    def get_cursos(self):
        self.c.execute("SELECT nome FROM cursos ORDER BY nome")
        return [row[0] for row in self.c.fetchall()]

    def adicionar_curso(self, nome_curso):
        nome_normalizado = self.normalizar_texto(nome_curso)
        cursos_normalizados = [self.normalizar_texto(c) for c in self.get_cursos()]

        if nome_normalizado in cursos_normalizados:
            return False

        try:
            self.c.execute("INSERT INTO cursos (nome) VALUES (?)", (nome_curso,))
            self.conn.commit()
            return True
        except Exception:
            return False

    def register_students(self, estudante):
        self.c.execute('''
            INSERT INTO estudantes (
                nome, email, telefone, sexo, data_nascimento, endereco, curso, picture
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', estudante)
        self.conn.commit()

    def view_all_students(self):
        self.c.execute('''
            SELECT id, nome, email, telefone, sexo, data_nascimento, endereco, curso, picture
            FROM estudantes
        ''')
        return self.c.fetchall()

    def search_student(self, id):
        self.c.execute('SELECT * FROM estudantes WHERE id = ?', (id,))
        return self.c.fetchone()

    def update_student(self, estudante):
        self.c.execute('''
            UPDATE estudantes SET
                nome=?, email=?, telefone=?, sexo=?, data_nascimento=?,
                endereco=?, curso=?, picture=?
            WHERE id=?
        ''', estudante)
        self.conn.commit()

    def delete_student(self, id):
        self.c.execute('DELETE FROM estudantes WHERE id=?', (id,))
        self.conn.commit()

    @staticmethod
    def normalizar_texto(texto):
        return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8').lower()

    @staticmethod
    def ler_imagem_como_blob(caminho_imagem):
        with open(caminho_imagem, 'rb') as file:
            return file.read()
