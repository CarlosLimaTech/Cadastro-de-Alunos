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
    
    def show_students(self, estudante):
        print(
            f'ID:{estudante[0]} | Nome: {estudante[1]} | email: {estudante[2]} | Telefone: {estudante[3]} | '
            f'Sexo: {estudante[4]} | Data de nascimento: {estudante[5]} | Endereço: {estudante[6]} | '
            f'Curso: {estudante[7]} | Foto: {estudante[8]}'
        )

    def register_students(self, estudantes):
        self.c.execute(
            "INSERT INTO estudantes "
            "(nome, email, telefone, sexo, data_nascimento, endereco, curso, picture) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (estudantes)
        )
        self.conn.commit

        messagebox.showinfo('Sucesso', 'Registro salvo com sucesso!')
    
    def view_all_students(self):
        self.c.execute("SELECT id, nome, email, telefone, sexo, data_nascimento, endereco, curso, picture FROM estudantes")
        dados = self.c.fetchall()

        return dados
    
    def search_student(self, id):
        self.c.execute(
            "SELECT * FROM estudantes WHERE id = ?", (id,))
        dados = self.c.fetchone()
        
        return dados

    def update_student(self, estudante):
        query = "UPDATE estudantes SET nome=?, email=?, telefone=?, sexo=?, data_nascimento=?, endereco=?, curso=?, picture=? WHERE id=?"
            
        self.c.execute(query, estudante)
        self.conn.commit()
        messagebox.showinfo('Sucesso', f'Estudante com ID: {estudante[8]} atulizado!')

    def delete_student(self, id):
        self.c.execute("DELETE FROM estudantes WHERE id=?", (id,))
        self.conn.commit()
        messagebox.showinfo('Sucesso', f'Estudante com ID: {id} deletado!')

sistemaDeCadastro = SistemaDeCadastro()