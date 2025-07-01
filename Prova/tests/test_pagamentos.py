import pytest
from unittest import mock
import json
from datetime import datetime

# Teste para obter um pagamento existente
def test_get_pagamento(client, mocker):
    # Mock de um pagamento
    pagamento_mock = (1, 123, "2023-05-15", 150.00, "cartão", "ref123", "pago")
    
    # Configurando o mock para simular o retorno do banco de dados
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = pagamento_mock
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    # Fazendo a requisição GET
    response = client.get('/pagamentos/1')
    
    # Verificando o resultado
    assert response.status_code == 200
    assert response.json['id_pagamento'] == 1
    assert response.json['id_aluno'] == 123
    assert response.json['valor'] == 150.00
    assert response.json['metodo_pagamento'] == "cartão"

# Teste para obter um pagamento que não existe
def test_get_pagamento_nao_encontrado(client, mocker):
    # Configurando o mock para simular que o pagamento não foi encontrado
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    # Fazendo a requisição GET
    response = client.get('/pagamentos/999')
    
    # Verificando o resultado
    assert response.status_code == 404
    assert "não encontrado" in response.json['error']

# Teste para adicionar um novo pagamento
def test_add_pagamento(client, mocker):
    # Dados do novo pagamento
    novo_pagamento = {
        "id_aluno": 123,
        "valor": 200.00,
        "data_pagamento": "2023-06-01",
        "metodo_pagamento": "pix"
    }
    
    # Configurando os mocks
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    # Mock para verificar se o aluno existe
    mock_cursor.fetchone.side_effect = [(123, "Nome do Aluno"), (1,)]  # Primeiro retorna o aluno, depois o ID do pagamento
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    # Fazendo a requisição POST
    response = client.post('/pagamentos', json=novo_pagamento)
    
    # Verificando o resultado
    assert response.status_code == 201
    assert "Pagamento adicionado" in response.json['message']
    assert 'id_pagamento' in response.json

# Teste para atualizar um pagamento existente
def test_update_pagamento(client, mocker):
    # Dados para atualização
    pagamento_atualizado = {
        "id_aluno": 123,
        "valor": 250.00,
        "data_pagamento": "2023-06-02",
        "metodo_pagamento": "boleto",
        "referencia": "ref456",
        "status": "pago"
    }
    
    # Configurando os mocks
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    # Mock para verificar se o pagamento existe
    mock_cursor.fetchone.return_value = (1, 123, "2023-05-15", 150.00, "cartão", "ref123", "pendente")
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    # Fazendo a requisição PUT
    response = client.put('/pagamentos/1', json=pagamento_atualizado)
    
    # Verificando o resultado
    assert response.status_code == 200
    assert "Pagamento atualizado" in response.json['message']

# Teste para deletar um pagamento existente
def test_delete_pagamento(client, mocker):
    # Configurando os mocks
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    # Mock para verificar se o pagamento existe
    mock_cursor.fetchone.return_value = (1, 123, "2023-05-15", 150.00, "cartão", "ref123", "pago")
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    # Fazendo a requisição DELETE
    response = client.delete('/pagamentos/1')
    
    # Verificando o resultado
    assert response.status_code == 200
    assert "Pagamento deletado" in response.json['message']

# Teste para tentar deletar um pagamento que não existe
def test_delete_pagamento_nao_encontrado(client, mocker):
    # Configurando os mocks
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    # Mock para simular que o pagamento não foi encontrado
    mock_cursor.fetchone.return_value = None
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    # Fazendo a requisição DELETE
    response = client.delete('/pagamentos/999')
    
    # Verificando o resultado
    assert response.status_code == 404
    assert "não encontrado" in response.json['error']