import pytest
import responses
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import api_client

@responses.activate
def test_buscar_endereco_por_cep_sucesso():
    # 1. Configuramos a simulação do serviço externo
    cep_teste = "01001000"
    url_esperada = f"https://viacep.com.br/ws/{cep_teste}/json/"
    
    resposta_simulada = {
        "cep": "01001-000",
        "logradouro": "Praça da Sé",
        "bairro": "Sé",
        "localidade": "São Paulo",
        "uf": "SP"
    }
    
    responses.add(responses.GET, url_esperada, json=resposta_simulada, status=200)
    
    resultado = api_client.buscar_endereco_por_cep(cep_teste)
    
    assert resultado is not None
    assert resultado["localidade"] == "São Paulo"
    assert resultado["uf"] == "SP"