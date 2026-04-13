import requests

def buscar_endereco_por_cep(cep):
    """Consome a API pública do ViaCEP para buscar a localidade."""
    cep = cep.replace("-", "").strip()
    if len(cep) != 8 or not cep.isdigit():
        return None
    
    url = f"https://viacep.com.br/ws/{cep}/json/"
    try:
        resposta = requests.get(url, timeout=5)
        if resposta.status_code == 200:
            dados = resposta.json()
            if "erro" not in dados:
                return dados
    except requests.RequestException:
        return None
    return None