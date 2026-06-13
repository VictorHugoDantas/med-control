import json
import os

FILE_PATH = "medicamentos.json"

def carregar_medicamentos():
    if not os.path.exists(FILE_PATH):
        return []
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def salvar_medicamentos(medicamentos):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(medicamentos, f, indent=4, ensure_ascii=False)

def adicionar_medicamento(nome, dosagem, horario):
    """Adiciona um novo medicamento à lista."""
    if not nome or not dosagem or not horario:
        raise ValueError("Nome, dosagem e horário são obrigatórios.")
    
    medicamentos = carregar_medicamentos()
    novo_med = {
        "nome": nome.strip(),
        "dosagem": dosagem.strip(),
        "horario": horario.strip()
    }
    medicamentos.append(novo_med)
    salvar_medicamentos(medicamentos)
    return novo_med

def listar_medicamentos():
    return carregar_medicamentos()

def remover_medicamento(nome):
    medicamentos = carregar_medicamentos()
    meds_filtrados = [m for m in medicamentos if m["nome"].lower() != nome.lower()]
    
    if len(medicamentos) == len(meds_filtrados):
        return False  
    
    salvar_medicamentos(meds_filtrados)
    return True
def salvar_novo_item(nome_item):
    try:
        # Envia um dado novo para a tabela do Supabase
        resposta = supabase.table("itens").insert({"nome": nome_item}).execute()
        print("Item cadastrado com sucesso!", resposta.data)
    except Exception as e:
        print("Erro ao salvar no banco:", e)

from src.supabase_client import supabase

def puxar_dados_do_banco():
    try:
        # Busca todos os dados da tabela 'itens'
        resposta = supabase.table("itens").select("*").execute()
        print("Dados do Banco:", resposta.data)
    except Exception as e:
        print("Erro ao conectar no Supabase:", e)

# Chame a função para testar se aparece no seu terminal
puxar_dados_do_banco()
