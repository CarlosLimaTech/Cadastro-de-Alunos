import unittest
from database.db_manager import SistemaDeCadastro
import os

class TestSistemaDeCadastro(unittest.TestCase):

    def setUp(self):
        self.db = SistemaDeCadastro(db_name=':memory:')

    def test_adicionar_curso(self):
        sucesso = self.db.adicionar_curso("Engenharia")
        self.assertTrue(sucesso)

        cursos = self.db.get_cursos()
        self.assertIn("Engenharia", cursos)

    def test_prevenir_curso_duplicado(self):
        self.db.adicionar_curso("ADS")
        sucesso = self.db.adicionar_curso("ads")
        self.assertFalse(sucesso)

    def test_register_and_search_student(self):
        aluno = ["João da Silva", "joao@email.com", "(11) 91234-5678", "M", "2000-01-01",
                 "Rua A", "ADS", "caminho/foto.png"]

        self.db.register_students(aluno)
        alunos = self.db.view_all_students()
        self.assertEqual(len(alunos), 1)

        aluno_id = alunos[0][0]
        buscado = self.db.search_student(aluno_id)
        self.assertIsNotNone(buscado)
        self.assertEqual(buscado[1], "João da Silva")

    def test_update_student(self):
        aluno = ["Maria Oliveira", "maria@email.com", "(11) 98765-4321", "F", "1999-05-10",
                 "Rua B", "Medicina", "foto2.png"]
        self.db.register_students(aluno)
        aluno_id = self.db.view_all_students()[0][0]

        dados_atualizados = ["Maria O.", "nova@maria.com", "(11) 91234-0000", "F", "1999-05-10",
                             "Rua Nova", "Medicina", "foto2_atual.png", aluno_id]
        self.db.update_student(dados_atualizados)

        aluno_modificado = self.db.search_student(aluno_id)
        self.assertEqual(aluno_modificado[1], "Maria O.")
        self.assertEqual(aluno_modificado[2], "nova@maria.com")

    def test_delete_student(self):
        aluno = ["Carlos Souza", "carlos@email.com", "(11) 90000-0000", "M", "2001-03-20",
                 "Rua C", "Engenharia", "img.png"]
        self.db.register_students(aluno)
        aluno_id = self.db.view_all_students()[0][0]

        self.db.delete_student(aluno_id)
        resultado = self.db.search_student(aluno_id)
        self.assertIsNone(resultado)
    
    def test_adicionar_curso_insensivel_acentos_maiusculas(self):
        self.db.adicionar_curso("Veterinária")
        resultado = self.db.adicionar_curso("veterinaria")
        self.assertFalse(resultado)

    def test_inserir_varios_alunos(self):
        alunos = [
            ["Ana Lins", "ana@email.com", "(11) 91234-0000", "F", "2002-01-01", "Rua A", "ADS", "foto1.png"],
            ["Bruno Souza", "bruno@email.com", "(11) 91234-1111", "M", "2001-01-01", "Rua B", "Medicina", "foto2.png"]
        ]
        for aluno in alunos:
            self.db.register_students(aluno)

        todos = self.db.view_all_students()
        self.assertEqual(len(todos), 2)

    def test_buscar_aluno_inexistente(self):
        resultado = self.db.search_student(9999)
        self.assertIsNone(resultado)

    def test_deletar_aluno_inexistente(self):
        try:
            self.db.delete_student(9999)
        except Exception as e:
            self.fail(f"Erro inesperado ao deletar aluno inexistente: {e}")
    def test_get_cursos_ordenado(self):
        self.db.adicionar_curso("Zoologia")
        self.db.adicionar_curso("Arquitetura")
        cursos = self.db.get_cursos()
        self.assertEqual(cursos, sorted(cursos))

if __name__ == '__main__':
    unittest.main()