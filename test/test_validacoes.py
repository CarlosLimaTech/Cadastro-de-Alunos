import unittest
from validacoes import (
    validar_nome_completo,
    validar_email,
    validar_telefone,
    validar_sexo,
    validar_endereco,
    validar_curso,
    normalizar_texto
)

class TestValidacoes(unittest.TestCase):

    def test_nome_completo_valido(self):
        self.assertTrue(validar_nome_completo("João Silva"))

    def test_nome_invalido_simples(self):
        self.assertFalse(validar_nome_completo("João"))

    def test_email_valido(self):
        self.assertTrue(validar_email("teste@email.com"))

    def test_email_invalido(self):
        self.assertFalse(validar_email("teste.com"))

    def test_telefone_valido_9_digitos(self):
        self.assertTrue(validar_telefone("(11) 91234-5678"))

    def test_telefone_valido_8_digitos(self):
        self.assertTrue(validar_telefone("(11) 1234-5678"))

    def test_telefone_invalido(self):
        self.assertFalse(validar_telefone("11912345678"))

    def test_sexo_valido_m(self):
        self.assertTrue(validar_sexo("M"))

    def test_sexo_valido_f(self):
        self.assertTrue(validar_sexo("f"))

    def test_sexo_invalido(self):
        self.assertFalse(validar_sexo("X"))

    def test_endereco_valido(self):
        self.assertTrue(validar_endereco("Rua 1"))

    def test_endereco_vazio(self):
        self.assertFalse(validar_endereco(""))

    def test_curso_existe(self):
        cursos = ["Engenharia", "ADS", "Medicina"]
        self.assertTrue(validar_curso("ads", cursos))

    def test_curso_invalido(self):
        cursos = ["Engenharia", "ADS", "Medicina"]
        self.assertFalse(validar_curso("Biologia", cursos))

    def test_normalizar_texto(self):
        self.assertEqual(normalizar_texto("Veterinária"), "veterinaria")
        self.assertEqual(normalizar_texto("Árvore"), "arvore")

if __name__ == '__main__':
    unittest.main()
