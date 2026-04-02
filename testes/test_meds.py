import pytest
import os
import sys

# Garante que a pasta 'src' seja reconhecida para podermos importar o med_manager
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import med_manager

# Nome de um arquivo temporário só para rodar os testes
TEST_FILE = "test_medicamentos.json"

@pytest.fixture(autouse=True)
def setup_e_teardown():
    """Muda o arquivo alvo antes do teste e limpa tudo depois que o teste acaba."""
    med_manager.FILE_PATH = TEST_FILE
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    yield  # Aqui o teste roda
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)

# TESTE 1: Caminho Feliz (A funcionalidade principal funciona?)
def test_adicionar_medicamento_com_sucesso():
    med_manager.adicionar_medicamento("Aspirina", "100mg", "12:00")
    lista = med_manager.listar_medicamentos()
    
    assert len(lista) == 1
    assert lista[0]["nome"] == "Aspirina"
    assert lista[0]["dosagem"] == "100mg"

# TESTE 2: Entrada Inválida (O sistema bloqueia dados incorretos?)
def test_adicionar_medicamento_com_dados_vazios():
    with pytest.raises(ValueError, match="Nome, dosagem e horário são obrigatórios."):
        med_manager.adicionar_medicamento("", "100mg", "12:00")

# TESTE 3: Caso Limite/Erro (O que acontece se tentar apagar o que não existe?)
def test_remover_medicamento_inexistente():
    # Tenta remover um remédio de uma lista vazia
    resultado = med_manager.remover_medicamento("Dipirona")
    
    # O esperado é que retorne False (indicando que não achou)
    assert resultado is False