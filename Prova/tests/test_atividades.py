import pytest
from unittest import mock

def test_get_atividade(client, mocker):
    atividade_mock = (1, "Prova de Matemática", "2023-06-15")
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = atividade_mock
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.get('/atividade/1')
    
    assert response.status_code == 200
    assert response.json['id_atividade'] == 1
    assert response.json['descricao'] == "Prova de Matemática"
    assert response.json['data_realizacao'] == "2023-06-15"

def test_get_atividade_nao_encontrada(client, mocker):
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.get('/atividade/999')
    
    assert response.status_code == 404
    assert "não encontrada" in response.json['error']

def test_add_atividade(client, mocker):
    nova_atividade = {
        "descricao": "Trabalho de História",
        "data_realizacao": "2023-06-20"
    }
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.post('/atividade', json=nova_atividade)
    
    assert response.status_code == 201
    assert "Atividade adicionada" in response.json['message']

def test_add_atividade_campos_obrigatorios(client):
    atividade_incompleta = {
        "descricao": "Trabalho incompleto"
    }
    
    response = client.post('/atividade', json=atividade_incompleta)
    
    assert response.status_code == 400
    assert "Campos obrigatórios" in response.json['error']

def test_update_atividade(client, mocker):
    atividade_atualizada = {
        "descricao": "Prova de Matemática - Atualizada",
        "data_realizacao": "2023-06-25"
    }
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.put('/atividade/1', json=atividade_atualizada)
    
    assert response.status_code == 200
    assert "Atividade atualizada" in response.json['message']

def test_delete_atividade(client, mocker):
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.delete('/atividade/1')
    
    assert response.status_code == 200
    assert "Atividade deletada" in response.json['message']