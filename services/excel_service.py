import pandas as pd
from dateutil import parser
from datetime import datetime
from validacoes import validar_dados_linha

def exportar_dados_para_excel(dados, caminho):
    dados_sem_imagem = []
    for linha in dados:
        linha_sem_img = list(linha[:-1])
        try:
            linha_sem_img[5] = datetime.strptime(linha_sem_img[5], "%Y-%m-%d").strftime("%d/%m/%Y")
        except:
            pass
        dados_sem_imagem.append(linha_sem_img)

    colunas = ['Id', 'Nome', 'Email', 'Telefone', 'Sexo', 'Data Nasc.', 'Endereço', 'Curso']
    df = pd.DataFrame(dados_sem_imagem, columns=colunas)
    df.to_excel(caminho, index=False)

def exportar_modelo_excel(caminho, colunas):
    df = pd.DataFrame(columns=colunas)
    df.to_excel(caminho, index=False)

def importar_planilha_excel(caminho, db, imagem_padrao, colunas_esperadas):
    df = pd.read_excel(caminho)
    df = df.map(lambda x: str(x).strip() if isinstance(x, str) else x)

    colunas_com_id = colunas_esperadas
    colunas_sem_id = colunas_esperadas[1:]

    if list(df.columns) == colunas_com_id:
        possui_id = True
    elif list(df.columns) == colunas_sem_id:
        possui_id = False
    else:
        raise ValueError("Colunas inválidas na planilha.")

    erros_detalhados = []
    inseridos = 0

    cursos_validos = db.get_cursos()

    for i, row in df.iterrows():
        linha_num = i + 2
        nome = row['Nome']
        email = row['Email']
        telefone = row['Telefone']
        sexo = row['Sexo']
        endereco = row['Endereço']
        curso = row['Curso']

        try:
            data_nasc_raw = row['Data Nasc.']
            if pd.isna(data_nasc_raw) or str(data_nasc_raw).strip() == '':
                raise ValueError("Data vazia")

            if isinstance(data_nasc_raw, (datetime, pd.Timestamp)):
                data = data_nasc_raw.strftime('%Y-%m-%d')
            else:
                parsed = parser.parse(str(data_nasc_raw), dayfirst=True)
                data = parsed.strftime('%Y-%m-%d')
        except Exception:
            erros_detalhados.append(f"Linha {linha_num}: Data de nascimento inválida ({data_nasc_raw})")
            continue

        falhas = validar_dados_linha(nome, email, telefone, sexo, endereco, curso, cursos_validos)
        if falhas:
            erros_detalhados.append(f"Linha {linha_num}: {nome or '---'} — campos inválidos: {', '.join(falhas)}")
            continue

        try:
            id_aluno = int(row['Id']) if possui_id else None
        except:
            id_aluno = None

        if id_aluno:
            db.update_student([nome, email, telefone, sexo, data, endereco, curso, imagem_padrao, id_aluno])
        else:
            db.register_students([nome, email, telefone, sexo, data, endereco, curso, imagem_padrao])

        inseridos += 1

    return inseridos, erros_detalhados
