import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
import pandas as pd
from ui.interface import InterfaceCadastro
import os

class TestImportacaoExcel(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

        imagem_path = os.path.join("assets", "icons", "Logo.png")

        self.interface = InterfaceCadastro(self.root)

        self.interface.imagem_path = imagem_path

        from PIL import Image, ImageTk
        logo_img = Image.open(imagem_path).resize((50, 50))
        self.interface.logo = ImageTk.PhotoImage(logo_img)

        self.interface.db = MagicMock()
        self.interface.db.get_cursos.return_value = ["Engenharia", "Medicina", "ADS"]
        self.interface.db.register_students = MagicMock()
        self.interface.db.update_student = MagicMock()

    def tearDown(self):
        self.root.destroy()

    @patch("pandas.read_excel")
    @patch("tkinter.filedialog.askopenfilename")
    def test_importar_novo_aluno(self, mock_file_dialog, mock_read_excel):
        mock_file_dialog.return_value = "fake.xlsx"
        mock_read_excel.return_value = pd.DataFrame([{
            "Id": None,
            "Nome": "João Silva",
            "Email": "joao@email.com",
            "Telefone": "(11) 91234-5678",
            "Sexo": "M",
            "Data Nasc.": "2000-01-01",
            "Endereço": "Rua A",
            "Curso": "Engenharia"
        }])

        self.interface.importar_excel()
        self.interface.db.register_students.assert_called_once()
        self.interface.db.update_student.assert_not_called()

    @patch("pandas.read_excel")
    @patch("tkinter.filedialog.askopenfilename")
    def test_importar_com_id_para_atualizar(self, mock_file_dialog, mock_read_excel):
        mock_file_dialog.return_value = "fake.xlsx"
        mock_read_excel.return_value = pd.DataFrame([{
            "Id": 1,
            "Nome": "Maria Silva",
            "Email": "maria@email.com",
            "Telefone": "(11) 93456-7890",
            "Sexo": "F",
            "Data Nasc.": "1998-05-15",
            "Endereço": "Rua B",
            "Curso": "Medicina"
        }])

        self.interface.importar_excel()
        self.interface.db.update_student.assert_called_once()
        self.interface.db.register_students.assert_not_called()

    @patch("pandas.read_excel")
    @patch("tkinter.filedialog.askopenfilename")
    def test_importar_dados_invalidos(self, mock_file_dialog, mock_read_excel):
        mock_file_dialog.return_value = "fake.xlsx"
        mock_read_excel.return_value = pd.DataFrame([{
            "Id": None,
            "Nome": "Carlos",
            "Email": "emailinvalido.com",
            "Telefone": "12345678",
            "Sexo": "X",
            "Data Nasc.": "2001-03-03",
            "Endereço": "",
            "Curso": "Física"
        }])

        self.interface.importar_excel()
        self.interface.db.register_students.assert_not_called()
        self.interface.db.update_student.assert_not_called()

    @patch("pandas.read_excel")
    @patch("tkinter.filedialog.askopenfilename")
    def test_importar_multiplos_alunos_validos_e_invalidos(self, mock_file_dialog, mock_read_excel):
        mock_file_dialog.return_value = "fake.xlsx"
        mock_read_excel.return_value = pd.DataFrame([
            {
                "Id": None,
                "Nome": "João Silva",
                "Email": "joao@email.com",
                "Telefone": "(11) 91234-5678",
                "Sexo": "M",
                "Data Nasc.": "2000-01-01",
                "Endereço": "Rua A",
                "Curso": "Engenharia"
            },
            {
                "Id": None,
                "Nome": "Ana",  # Inválido
                "Email": "ana@email.com",
                "Telefone": "(11) 91234-5678",
                "Sexo": "F",
                "Data Nasc.": "2001-02-02",
                "Endereço": "Rua B",
                "Curso": "Engenharia"
            },
            {
                "Id": 2,
                "Nome": "Carlos Silva",
                "Email": "carlos@email.com",
                "Telefone": "(11) 93333-4444",
                "Sexo": "M",
                "Data Nasc.": "1999-04-04",
                "Endereço": "Rua C",
                "Curso": "Medicina"
            },
            {
                "Id": None,
                "Nome": "Lucia Vieira",
                "Email": "lucia@",  # Inválido
                "Telefone": "0000",  # Inválido
                "Sexo": "F",
                "Data Nasc.": "2001-01-01",
                "Endereço": "Rua D",
                "Curso": "Engenharia"
            }
        ])

        self.interface.importar_excel()
        self.assertEqual(self.interface.db.register_students.call_count, 1)
        self.assertEqual(self.interface.db.update_student.call_count, 1)

    @patch("pandas.read_excel")
    @patch("tkinter.filedialog.askopenfilename")
    def test_importar_com_id_sobrescreve_dados(self, mock_file_dialog, mock_read_excel):
        mock_file_dialog.return_value = "fake.xlsx"
        mock_read_excel.return_value = pd.DataFrame([{
            "Id": 5,
            "Nome": "Aluno Atualizado",
            "Email": "novo@email.com",
            "Telefone": "(11) 99999-8888",
            "Sexo": "F",
            "Data Nasc.": "1990-12-12",
            "Endereço": "Rua Z",
            "Curso": "Medicina"
        }])

        self.interface.importar_excel()
        self.interface.db.update_student.assert_called_once()
        args = self.interface.db.update_student.call_args[0][0]
        self.assertEqual(args[-1], 5)
        self.assertEqual(args[0], "Aluno Atualizado")


if __name__ == "__main__":
    unittest.main()