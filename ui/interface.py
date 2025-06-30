from datetime import date, datetime
from dateutil import parser
import sys, os
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from database.db_manager import SistemaDeCadastro
from validacoes import (
    validar_nome_completo,
    validar_email,
    validar_telefone,
    validar_sexo,
    validar_endereco,
    normalizar_texto,
    validar_curso
)
import pandas as pd
from tkinter import filedialog
from io import BytesIO
from tkinter import scrolledtext

def resource_path(relative_path):
    try:
        return os.path.join(sys._MEIPASS, relative_path)
    except:
        return os.path.join(os.path.abspath("."), relative_path)

class InterfaceCadastro:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Alunos")
        self.root.geometry('810x550')
        self.root.configure(background='#feffff')
        self.root.resizable(width=False, height=False)
        self.id_atual = None

        self.db = SistemaDeCadastro()
        self.imagem_path = resource_path('assets/icons/Logo.png')

        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")

        self.criar_frames()
        self.criar_widgets()
        self.mostrar_alunos()

    def criar_frames(self):
        self.frame_logo = Frame(self.root, width=850, height=52, bg='#146C94')
        self.frame_logo.grid(row=0, column=0, columnspan=5, sticky=NSEW)

        self.frame_botoes = Frame(self.root, width=100, height=200, bg='#feffff', relief=RAISED)
        self.frame_botoes.grid(row=1, column=0, sticky=NSEW)

        self.frame_detalhes = Frame(self.root, width=800, height=180, bg='#feffff', relief=SOLID)
        self.frame_detalhes.grid(row=1, column=1, padx=10, sticky=NSEW)

        self.frame_tabela = Frame(self.root, width=800, height=100, bg='#feffff', relief=SOLID)
        self.frame_tabela.grid(row=3, column=0, columnspan=5, sticky=NSEW, padx=10)

    def criar_widgets(self):
        # Logo
        logo_img = Image.open(self.imagem_path).resize((50, 50))
        self.logo = ImageTk.PhotoImage(logo_img)
        Label(self.frame_logo, image=self.logo, text=" Cadastro de Alunos", compound=LEFT, anchor=NW,
              font=('Verdana 15'), bg='#146C94', fg='#feffff').place(x=5, y=0)

        # Foto do aluno
        self.img = ImageTk.PhotoImage(Image.open(self.imagem_path).resize((130, 130)))
        self.img_label = Label(self.frame_detalhes, image=self.img, bg='#feffff')
        self.img_label.place(x=390, y=10)

        # Entradas
        self.e_nome = self._criar_entry("Nome *", 4, 10, 7, 40)
        self.e_email = self._criar_entry("Email *", 4, 70, 7, 100)
        self.e_telefone = self._criar_entry("Telefone *", 4, 130, 7, 160, width=15)

        Label(self.frame_detalhes, text="Sexo *", font=('Ivy 10'), bg='#feffff').place(x=127, y=130)
        self.c_sexo = ttk.Combobox(self.frame_detalhes, values=["M", "F"], width=7, font=('Ivy 8'), justify='center')
        self.c_sexo.place(x=130, y=160)

        Label(self.frame_detalhes, text="Data de nascimento *", font=('Ivy 10'), bg='#feffff').place(x=220, y=10)
        self.data_nascimento = DateEntry(self.frame_detalhes, width=15, justify='center',
                                 background='darkblue', foreground='white',
                                 borderwidth=2, year=2025, date_pattern='dd/mm/yyyy')
        self.data_nascimento.place(x=224, y=40)

        self.e_endereco = self._criar_entry("Endereço *", 220, 70, 224, 100, width=18)

        Label(self.frame_detalhes, text="Curso *", font=('Ivy 10'), bg='#feffff').place(x=220, y=130)
        cursos = self.db.get_cursos()
        self.c_curso = ttk.Combobox(self.frame_detalhes, values=cursos, width=15, font=('Ivy 8'), justify='center')
        self.c_curso.place(x=224, y=160)
        self.carregar_cursos()
        btn_add_curso = Button(self.frame_detalhes, text="+", command=self.abrir_popup_curso, width=2, font=('Ivy 7 bold'), bg="#e1e1e1")
        btn_add_curso.place(x=340, y=160)

        # Botão carregar imagem
        self.botao_carregar = Button(self.frame_detalhes, command=self.escolher_imagem,
                                     text='Carregar Foto', width=20, font=('Ivy 7 bold'), bg='#feffff')
        self.botao_carregar.place(x=390, y=160)

        # Frame de busca
        frame_procurar = Frame(self.frame_botoes, bg='#feffff')
        frame_procurar.grid(row=0, column=0, pady=10, padx=10)

        Label(frame_procurar, text="Procurar aluno por Id", font=('Ivy 10'), bg='#feffff').grid(row=0, column=0, sticky=W)
        self.e_procurar = Entry(frame_procurar, width=20, justify='center', relief='solid')
        self.e_procurar.grid(row=1, column=0, pady=5)

        Button(frame_procurar, command=self.procurar, text='Procurar', font=('Ivy 7 bold'), bg='#feffff').grid(row=1, column=1)

        # Botões de ação
        self.botao_adicionar = self._criar_botao("  Adicionar", self.adicionar, 'add.png', 1)
        self.botao_update = self._criar_botao("  Atualizar ", self.atualizar, 'update.png', 2)
        self.botao_delete = self._criar_botao("  Deletar   ", self.deletar, 'del.png', 3)
        self.botao_excel = self._criar_botao("  Importar/Exportar", self.abrir_popup_excel, 'excel.png', 4)

        #Desativando os botões no início
        self.botao_adicionar.config(state=NORMAL)
        self.botao_update.config(state=DISABLED)
        self.botao_delete.config(state=DISABLED)

    def _criar_entry(self, texto, x1, y1, x2, y2, width=30):
        Label(self.frame_detalhes, text=texto, font=('Ivy 10'), bg='#feffff').place(x=x1, y=y1)
        entry = Entry(self.frame_detalhes, width=width, justify='left', relief='solid')
        entry.place(x=x2, y=y2)
        return entry

    def _criar_botao(self, texto, comando, icone, linha):
        img = ImageTk.PhotoImage(Image.open(resource_path(f'assets/icons/{icone}')).resize((25, 25)))
        btn = Button(self.frame_botoes, command=comando, image=img, text=f'  {texto}', width=100,
                    compound=LEFT, font=('Ivy 11'), bg='#feffff')
        btn.image = img
        btn.grid(row=linha, column=0, pady=5, padx=10, sticky=NSEW)
        return btn


    def escolher_imagem(self):
        imagem_path = filedialog.askopenfilename()
        if imagem_path:
            self.imagem_path = imagem_path
            nova_img = ImageTk.PhotoImage(Image.open(imagem_path).resize((130, 130)))
            self.img_label.configure(image=nova_img)
            self.img_label.image = nova_img
            self.botao_carregar.config(text="Trocar Foto")

    def limpar_campos(self):
        for campo in [self.e_nome, self.e_email, self.e_telefone, self.e_endereco, self.e_procurar]:
            campo.delete(0, END)
        for combo in [self.c_sexo, self.c_curso]:
            combo.set('')
        self.data_nascimento.set_date(date.today())
        self.imagem_path = resource_path('assets/icons/Logo.png')
        nova_img = ImageTk.PhotoImage(Image.open(self.imagem_path).resize((130, 130)))
        self.img_label.configure(image=nova_img)
        self.img_label.image = nova_img
        self.id_atual = None
        self.desativar_botoes_edicao()
        self.carregar_cursos()

    def adicionar(self):
        nome = self.e_nome.get()
        email = self.e_email.get()
        telefone = self.e_telefone.get()
        sexo = self.c_sexo.get()
        data = datetime.strptime(self.data_nascimento.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
        endereco = self.e_endereco.get()
        curso = self.c_curso.get()
        imagem_blob = SistemaDeCadastro.ler_imagem_como_blob(self.imagem_path)

        # Verificação de campos obrigatórios
        if '' in [nome, email, telefone, sexo, data, endereco, curso]:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        if not validar_nome_completo(nome):
            messagebox.showerror("Erro", "Informe o nome completo (nome e sobrenome).")
            return

        if not validar_email(email):
            messagebox.showerror("Erro", "E-mail inválido.")
            return

        if not validar_telefone(telefone):
            messagebox.showerror("Erro", "Telefone deve estar no formato (XX) XXXXX-XXXX.")
            return

        if not validar_sexo(sexo):
            messagebox.showerror("Erro", "Sexo deve ser 'M' ou 'F'.")
            return

        if not validar_endereco(endereco):
            messagebox.showerror("Erro", "Endereço não pode estar vazio.")
            return

        if not validar_curso(curso, self.db.get_cursos()):
            messagebox.showerror("Erro", "Curso inválido.")
            return

        self.db.register_students([
            nome, email, telefone, sexo, data, endereco, curso, imagem_blob
        ])
        self.limpar_campos()
        self.mostrar_alunos()

    def procurar(self):
        try:
            id_texto = self.e_procurar.get().strip()
            if not id_texto.isdigit():
                messagebox.showerror("Erro", "Informe um ID numérico válido.")
                return

            id_aluno = int(id_texto)
            aluno = self.db.search_student(id_aluno)

            if not aluno:
                messagebox.showerror("Erro", "Aluno não encontrado.")
                return

            self.e_nome.delete(0, END)
            self.e_email.delete(0, END)
            self.e_telefone.delete(0, END)
            self.e_endereco.delete(0, END)

            self.e_nome.insert(0, aluno[1])
            self.e_email.insert(0, aluno[2])
            self.e_telefone.insert(0, aluno[3])
            self.c_sexo.set(aluno[4])
            data_formatada = datetime.strptime(aluno[5], "%Y-%m-%d").strftime("%d/%m/%Y")
            self.data_nascimento.set_date(data_formatada)
            self.e_endereco.insert(0, aluno[6])
            self.c_curso.set(aluno[7])

            imagem_blob = aluno[8]
            if imagem_blob:
                imagem_pil = Image.open(BytesIO(imagem_blob))
                nova_img = ImageTk.PhotoImage(imagem_pil.resize((130, 130)))
                self.img_label.configure(image=nova_img)
                self.img_label.image = nova_img

            self.id_atual = aluno[0]
            self.e_procurar.delete(0, END)
            self.botao_adicionar.config(state=DISABLED)
            self.botao_update.config(state=NORMAL)
            self.botao_delete.config(state=NORMAL)

        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro inesperado: {e}")


    def atualizar(self):
        try:
            if self.id_atual is None:
                messagebox.showerror("Erro", "Nenhum aluno selecionado para atualizar.")
                return

            nome = self.e_nome.get()
            email = self.e_email.get()
            telefone = self.e_telefone.get()
            sexo = self.c_sexo.get()
            data = datetime.strptime(self.data_nascimento.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
            endereco = self.e_endereco.get()
            curso = self.c_curso.get()
            imagem_blob = SistemaDeCadastro.ler_imagem_como_blob(self.imagem_path)

            if '' in [nome, email, telefone, sexo, data, endereco, curso]:
                messagebox.showerror("Erro", "Preencha todos os campos.")
                return
            
            if not validar_nome_completo(nome):
                messagebox.showerror("Erro", "Informe o nome completo (nome e sobrenome).")
                return

            if not validar_email(email):
                messagebox.showerror("Erro", "E-mail inválido.")
                return

            if not validar_telefone(telefone):
                messagebox.showerror("Erro", "Telefone deve estar no formato (XX) XXXXX-XXXX.")
                return

            if not validar_sexo(sexo):
                messagebox.showerror("Erro", "Sexo deve ser 'M' ou 'F'.")
                return

            if not validar_endereco(endereco):
                messagebox.showerror("Erro", "Endereço não pode estar vazio.")
                return

            if not validar_curso(curso, self.db.get_cursos()):
                messagebox.showerror("Erro", "Curso inválido.")
                return

            dados = [nome, email, telefone, sexo, data, endereco, curso, imagem_blob, self.id_atual]
            self.db.update_student(dados)
            self.limpar_campos()
            self.desativar_botoes_edicao()
            self.mostrar_alunos()

        except ValueError:
            messagebox.showerror("Erro", "ID inválido.")

    def deletar(self):
        try:
            if self.id_atual is None:
                messagebox.showerror("Erro", "Nenhum aluno selecionado para deletar.")
                return
            self.db.delete_student(self.id_atual)
            self.limpar_campos()
            self.desativar_botoes_edicao()
            self.mostrar_alunos()
        except ValueError:
            messagebox.showerror("Erro", "ID inválido.")

    def mostrar_alunos(self):
        list_header = ['Id', 'Nome', 'Email', 'Telefone', 'Sexo', 'Data', 'Endereço', 'Curso']

        df_list = self.db.view_all_students()

        tree_aluno = ttk.Treeview(self.frame_tabela, selectmode='extended', columns=list_header, show="headings")

        vsb = ttk.Scrollbar(self.frame_tabela, orient="vertical", command=tree_aluno.yview)
        hsb = ttk.Scrollbar(self.frame_tabela, orient="horizontal", command=tree_aluno.xview)

        tree_aluno.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        tree_aluno.grid(column=0, row=1, sticky='nsew')
        vsb.grid(column=1, row=1, sticky='ns')
        hsb.grid(column=0, row=2, sticky='ew')

        hd = ["nw", "nw", "nw", "center", "center", "center", "center", "center", "center" ]
        h = [40, 150, 150, 70, 70, 70, 120, 100, 100]
        n = 0

        for coluna in list_header:
            tree_aluno.heading(coluna, text=coluna.title(), anchor=NW)
            tree_aluno.column(coluna, width=h[n], anchor=hd[n])

            n+=1

        for item in df_list:
            item = list(item)
            try:
                item[5] = datetime.strptime(item[5], "%Y-%m-%d").strftime("%d/%m/%Y")
            except:
                pass
            tree_aluno.insert('', 'end', values=item)


    def desativar_botoes_edicao(self):
        self.botao_adicionar.config(state=NORMAL)
        self.botao_update.config(state=DISABLED)
        self.botao_delete.config(state=DISABLED)

    def carregar_cursos(self):
        cursos = self.db.get_cursos()
        self.c_curso['values'] = cursos

    def abrir_popup_curso(self):
        def salvar():
            nome = entrada.get().strip()
            if nome == "":
                messagebox.showwarning("Aviso", "O nome do curso não pode estar vazio.")
                return

            cursos_existentes = self.db.get_cursos()
            if normalizar_texto(nome) in [normalizar_texto(c) for c in cursos_existentes]:
                messagebox.showinfo("Aviso", "Esse curso já existe.")
                return

            sucesso = self.db.adicionar_curso(nome)
            if sucesso:
                messagebox.showinfo("Sucesso", f"Curso '{nome}' adicionado com sucesso.")
                self.carregar_cursos()  # Atualiza o combobox
                popup.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao adicionar curso.")

        popup = Toplevel(self.root)
        popup.title("Adicionar novo curso")
        popup.geometry("300x100")
        popup.resizable(False, False)

        Label(popup, text="Nome do curso:").grid(row=0, column=0, sticky='w', padx=10, pady=(10, 2))
        entrada = Entry(popup, width=30)
        entrada.grid(row=1, column=0, padx=10, pady=(0, 5))
        Button(popup, text="Salvar", command=salvar).grid(row=2, column=0, sticky='w', padx=10, pady=(0, 10))

    def exportar_excel(self):
        dados = self.db.view_all_students()
        if not dados:
            messagebox.showinfo("Aviso", "Não há dados para exportar.")
            return

        dados_sem_imagem = []
        for linha in dados:
            linha_sem_img = list(linha[:-1])  # remove imagem (última coluna)
            try:
                linha_sem_img[5] = datetime.strptime(linha_sem_img[5], "%Y-%m-%d").strftime("%d/%m/%Y")
            except:
                pass 
            dados_sem_imagem.append(linha_sem_img)

        colunas = ['Id', 'Nome', 'Email', 'Telefone', 'Sexo', 'Data Nasc.', 'Endereço', 'Curso']
        df = pd.DataFrame(dados_sem_imagem, columns=colunas)

        caminho = filedialog.asksaveasfilename(
            defaultextension='.xlsx',
            filetypes=[('Planilha Excel', '*.xlsx')],
            title='Salvar dados'
        )
        if caminho:
            try:
                df.to_excel(caminho, index=False)
                messagebox.showinfo("Sucesso", "Exportação concluída!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar: {e}")
    
    def abrir_popup_excel(self):
        popup = Toplevel(self.root)
        popup.title("Importar / Exportar Excel")
        popup.geometry("300x160")
        popup.resizable(False, False)

        Label(popup, text="Escolha uma opção:", font=('Ivy 10 bold')).pack(pady=10)

        Button(popup, text="Exportar todos os dados", font=('Ivy 10'), width=30, command=lambda: [popup.destroy(), self.exportar_excel()]).pack(pady=3)
        Button(popup, text="Baixar modelo em branco", font=('Ivy 10'), width=30, command=lambda: [popup.destroy(), self.exportar_modelo_excel()]).pack(pady=3)
        Button(popup, text="Importar planilha preenchida", font=('Ivy 10'), width=30, command=lambda: [popup.destroy(), self.importar_excel()]).pack(pady=3)

    def exportar_modelo_excel(self):
        colunas = ['Id', 'Nome', 'Email', 'Telefone', 'Sexo', 'Data Nasc.', 'Endereço', 'Curso']
        df = pd.DataFrame(columns=colunas)

        caminho = filedialog.asksaveasfilename(
            defaultextension='.xlsx',
            filetypes=[('Planilha Excel', '*.xlsx')],
            title='Salvar modelo'
        )
        if caminho:
            try:
                df.to_excel(caminho, index=False)
                messagebox.showinfo("Sucesso", "Modelo salvo com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar modelo: {e}")

    def importar_excel(self):
        caminho = filedialog.askopenfilename(
            filetypes=[("Planilhas Excel", "*.xlsx")],
            title="Selecione a planilha preenchida"
        )

        if not caminho:
            return

        try:
            df = pd.read_excel(caminho)

            df = df.map(lambda x: str(x).strip() if isinstance(x, str) else x)

            colunas_com_id = ['Id', 'Nome', 'Email', 'Telefone', 'Sexo', 'Data Nasc.', 'Endereço', 'Curso']
            colunas_sem_id = colunas_com_id[1:]

            possui_id = False
            if list(df.columns) == colunas_com_id:
                possui_id = True
            elif list(df.columns) != colunas_sem_id:
                messagebox.showerror("Erro", "Colunas inválidas na planilha.\nEsperado:\n" +
                                    ', '.join(colunas_com_id) + "\nOu:\n" + ', '.join(colunas_sem_id))
                return

            erros_detalhados = []
            inseridos = 0

            for i, row in df.iterrows():
                linha_num = i + 2
                nome = row['Nome']
                email = row['Email']
                telefone = row['Telefone']
                sexo = row['Sexo']
                endereco = row['Endereço']
                curso = row['Curso']

                data_nasc_raw = row['Data Nasc.']
                try:
                    if pd.isna(data_nasc_raw) or str(data_nasc_raw).strip() == '':
                        raise ValueError("Data vazia")

                    if isinstance(data_nasc_raw, (datetime, pd.Timestamp)):
                        data = data_nasc_raw.strftime('%Y-%m-%d')
                    else:
                        parsed = parser.parse(str(data_nasc_raw), dayfirst=True)
                        data = parsed.strftime('%Y-%m-%d')
                except Exception as e:
                    erros_detalhados.append(f"Linha {linha_num}: Data de nascimento inválida ({data_nasc_raw})")
                    continue

                imagem = SistemaDeCadastro.ler_imagem_como_blob(resource_path('assets/icons/Logo.png'))

                falhas = []
                if not validar_nome_completo(nome): falhas.append('Nome')
                if not validar_email(email): falhas.append('Email')
                if not validar_telefone(telefone): falhas.append('Telefone')
                if not validar_sexo(sexo): falhas.append('Sexo')
                if not validar_endereco(endereco): falhas.append('Endereço')
                if not validar_curso(curso, self.db.get_cursos()): falhas.append('Curso')

                if falhas:
                    erros_detalhados.append(f"Linha {linha_num}: {nome or '---'} — campos inválidos: {', '.join(falhas)}")
                    continue

                id_str = row.get('Id')
                try:
                    id_aluno = int(id_str)
                    self.db.update_student([
                        nome, email, telefone, sexo, data, endereco, curso, imagem, id_aluno
                    ])
                except (ValueError, TypeError):
                    self.db.register_students([
                        nome, email, telefone, sexo, data, endereco, curso, imagem
                    ])

                inseridos += 1

            self.mostrar_alunos()

            msg = f"Alunos inseridos/atualizados: {inseridos}\nFalhas: {len(erros_detalhados)}"
            if erros_detalhados:
                msg += "\n\nDetalhes:\n" + "\n".join(erros_detalhados)
                self._mostrar_erro_detalhado(msg)
            else:
                messagebox.showinfo("Importação concluída", msg)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao importar: {e}")


    def _mostrar_erro_detalhado(self, texto):
        popup = Toplevel(self.root)
        popup.title("Falhas na Importação")
        popup.geometry("500x400")
        popup.resizable(False, False)

        Label(popup, text="Alguns registros não foram importados:", font=('Ivy 10 bold')).pack(pady=(10, 5))

        text_area = scrolledtext.ScrolledText(popup, wrap='word', width=60, height=20)
        text_area.insert('1.0', texto)
        text_area.config(state='disabled')
        text_area.pack(padx=10, pady=5)

def main():
    root = Tk()
    InterfaceCadastro(root)
    root.mainloop()
