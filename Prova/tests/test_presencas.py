import pytest
from unittest import mock

def test_get_presenca(client, mocker):
    presenca_mock = (1, 123, "2023-06-01", True)
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = presenca_mock
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.get('/presencas/1')
    
    assert response.status_code == 200
    assert response.json['id_presenca'] == 1
    assert response.json['id_aluno'] == 123
    assert response.json['data_presenca'] == "2023-06-01"
    assert response.json['presente'] == True

def test_get_presenca_nao_encontrada(client, mocker):
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.get('/presencas/999')
    
    assert response.status_code == 404
    assert "não encontrada" in response.json['error']

def test_add_presenca(client, mocker):
    nova_presenca = {
        "id_aluno": 123,
        "data_presenca": "2023-06-01",
        "presente": True
    }
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (123, "João Silva")
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.post('/presencas', json=nova_presenca)
    
    assert response.status_code == 201
    assert "Presença adicionada" in response.json['message']

def test_add_presenca_campos_obrigatorios(client):
    presenca_incompleta = {
        "id_aluno": 123
    }
    
    response = client.post('/presencas', json=presenca_incompleta)
    
    assert response.status_code == 400
    assert "Campos obrigatórios" in response.json['error']

def test_update_presenca(client, mocker):
    presenca_atualizada = {
        "id_aluno": 123,
        "data_presenca": "2023-06-02",
        "presente": False
    }
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.put('/presencas/1', json=presenca_atualizada)
    
    assert response.status_code == 200
    assert "Presença atualizada" in response.json['message']

def test_delete_presenca(client, mocker):
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.delete('/presencas/1')
    
    assert response.status_code == 200
    assert "Presença deletada" in response.json['message']