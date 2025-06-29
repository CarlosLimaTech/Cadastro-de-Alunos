import sqlite3

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
                picture TEXT NOT NULL
            )
        ''')
        self.conn.commit()

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
