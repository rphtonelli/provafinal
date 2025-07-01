import pytest
from unittest import mock

def test_get_turma(client, mocker):
    turma_mock = (1, "Turma A", 1, "08:00-12:00")
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = turma_mock
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.get('/turmas/1')
    
    assert response.status_code == 200
    assert response.json['id_turma'] == 1
    assert response.json['nome_turma'] == "Turma A"
    assert response.json['id_professor'] == 1

def test_get_turma_nao_encontrada(client, mocker):
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.get('/turmas/999')
    
    assert response.status_code == 404
    assert "não encontrada" in response.json['error']

def test_add_turma(client, mocker):
    nova_turma = {
        "nome_completo": "João Silva",
        "nome_turma": "Turma B",
        "horario": "14:00-18:00"
    }
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (1,)  # Professor encontrado
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.post('/turmas', json=nova_turma)
    
    assert response.status_code == 201
    assert "Turma adicionada" in response.json['message']

def test_update_turma(client, mocker):
    turma_atualizada = {
        "nome_turma": "Turma A Atualizada",
        "id_professor": 2,
        "horario": "09:00-13:00"
    }
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.put('/turmas/1', json=turma_atualizada)
    
    assert response.status_code == 200
    assert "Turma atualizada" in response.json['message']

def test_delete_turma(client, mocker):
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.delete('/turmas/1')
    
    assert response.status_code == 200
    assert "Turma deletada" in response.json['message']