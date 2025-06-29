import re
import unicodedata

def validar_nome_completo(nome):
    return len(nome.strip().split()) >= 2

def validar_email(email):
    padrao = r"[^@]+@[^@]+\.[^@]+"
    return bool(re.fullmatch(padrao, email))

def validar_telefone(telefone):
    padrao = r"\(\d{2}\) \d{4,5}-\d{4}"
    return bool(re.fullmatch(padrao, telefone))

def validar_sexo(sexo):
    return sexo.upper() in ['M', 'F']

def validar_endereco(endereco):
    return endereco.strip() != ""

def normalizar_texto(texto):
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8').lower()

def validar_curso(curso, cursos_disponiveis):
    curso_normalizado = normalizar_texto(curso)
    cursos_normalizados = [normalizar_texto(c) for c in cursos_disponiveis]
    return curso_normalizado in cursos_normalizados