# 📘 Cadastro de Alunos
Sistema completo para cadastro, consulta, atualização, exclusão e importação/exportação de dados de estudantes, com interface gráfica (Tkinter), persistência em banco de dados SQLite e suporte a planilhas Excel.

## 📌 Funcionalidades
- Cadastro de estudantes com:
  - Nome, e-mail, telefone, sexo, data de nascimento, endereço, curso e foto
- Edição, exclusão e consulta individual
- Validações inteligentes para dados obrigatórios e formatos
- Importação de planilhas Excel (.xlsx) com modelo pronto para uso
- Exportação de dados para Excel
- Adição dinâmica de novos cursos
- Interface amigável desenvolvida com `Tkinter` e `ttk`
- Testes automatizados com `unittest`

## 🖼️ Interface
![Interface do sistema](![image](https://github.com/user-attachments/assets/0c63dfb8-a83c-4570-ad70-f658ebb832d9)


🧪 Testes
Para rodar todos os testes automatizados:
- python run_tests.py

🗂️ Estrutura do Projeto
cadastro-de-alunos/
├── assets/icons/              # Ícones para a interface
├── build/                     # (gerado pelo PyInstaller)
├── database/db_manager.py     # CRUD com SQLite
├── dist/main/                 # Executável gerado
├── services/excel_service.py  # Importação/exportação de Excel
├── test/                      # Testes unitários
├── ui/interface.py            # Interface gráfica (Tkinter)
├── validacoes.py              # Funções de validação
├── main.py                    # Ponto de entrada da aplicação
├── run_tests.py               # Runner dos testes
└── README.md

📋 Modelo de Planilha
Você pode:
- Exportar os dados atuais para uma planilha
- Baixar um modelo em branco
- Importar planilhas preenchidas com dados
- 
Colunas esperadas na planilha:
Id | Nome | Email | Telefone | Sexo | Data Nasc. | Endereço | Curso
OBS - O campo Id pode ser deixado em branco para novos cadastros.

