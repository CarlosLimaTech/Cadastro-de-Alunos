import sqlite3
from tkinter import messagebox

class SistemaDeCadastro:
    def __init__(self):
        self.conn = sqlite3.connect('estudantes.db')
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS estudantes (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       nome TEXT NOT NULL,
                       email TEXT NOT NULL,
                       telefone TEXT NOT NULL,
                       sexo TEXT NOT NULL,
                       data_nascimento TEXT NOT NULL,
                       endereco TEXT NOT NULL,
                       curso TEXT NOT NULL,
                       picture TEXT NOT NULL)''')
    
    def register_students(self, estudantes):
        self.c.execute(
            "INSERT INTO estudantes("
            "nome, email, telefone, sexo, data_nascimento, endereco, curso, picture"
            ") VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (estudantes)
        )
        self.conn.commit

        messagebox.showinfo('Sucesso', 'Registro salvo com sucesso!')
    
    def view_all_students(self):
        self.c.execute("SELECT id, nome, email, telefone, sexo, data_nascimento, endereco, curso, picture FROM estudantes")
        dados = self.c.fetchall()

        for dado in dados:
            print(
                f'ID:{dado[0]} | Nome: {dado[1]} | email: {dado[2]} | Telefone: {dado[3]} | '
                f'Sexo: {dado[4]} | Data de nascimento: {dado[5]} | Endereço: {dado[6]} | '
                f'Curso: {dado[7]} | Foto: {dado[8]}'
                )
    
    def search_student(self, id):
        self.c.execute(
            "SELECT id, nome, email, telefone, sexo, data_nascimento, endereco, curso, picture "
            "FROM estudantes"
            "WHERE id=?"
            (id))
        dados = self.c.fetchall()
        messagebox.showinfo('Sucesso', 'Registro com sucesso')