import pytest
from unittest import mock

def test_get_professor(client, mocker):
    professor_mock = (1, "João Silva", "joao@email.com", "11999999999")
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = professor_mock
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.get('/professores/1')
    
    assert response.status_code == 200
    assert response.json['id_professor'] == 1
    assert response.json['nome_completo'] == "João Silva"
    assert response.json['email'] == "joao@email.com"

def test_get_professor_nao_encontrado(client, mocker):
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.get('/professores/999')
    
    assert response.status_code == 404
    assert "não encontrado" in response.json['error']

def test_add_professor(client, mocker):
    novo_professor = {
        "nome_completo": "Maria Santos",
        "email": "maria@email.com",
        "telefone": "11888888888"
    }
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.post('/professores', json=novo_professor)
    
    assert response.status_code == 201
    assert "Professor adicionado" in response.json['message']

def test_add_professor_campos_obrigatorios(client, mocker):
    professor_incompleto = {
        "nome_completo": "Maria Santos"
        # Faltando email e telefone
    }
    
    response = client.post('/professores', json=professor_incompleto)
    
    assert response.status_code == 400
    assert "Campos obrigatórios" in response.json['error']

def test_update_professor(client, mocker):
    professor_atualizado = {
        "nome_completo": "João Silva Jr",
        "email": "joao.jr@email.com",
        "telefone": "11777777777"
    }
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.put('/professores/1', json=professor_atualizado)
    
    assert response.status_code == 200
    assert "Professor atualizado" in response.json['message']

def test_delete_professor(client, mocker):
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.delete('/professores/1')
    
    assert response.status_code == 200
    assert "Professor deletado" in response.json['message']

def test_add_professor_email_invalido(client, mocker):
    professor_email_invalido = {
        "nome_completo": "João Silva",
        "email": "email_invalido",
        "telefone": "11999999999"
    }
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Email inválido")
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.post('/professores', json=professor_email_invalido)
    
    assert response.status_code == 500
    assert "error" in response.json

def test_add_professor_telefone_invalido(client, mocker):
    professor_telefone_invalido = {
        "nome_completo": "João Silva",
        "email": "joao@email.com",
        "telefone": "123"  # Telefone muito curto
    }
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Telefone inválido")
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.post('/professores', json=professor_telefone_invalido)
    
    assert response.status_code == 500
    assert "error" in response.json