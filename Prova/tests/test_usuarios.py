import pytest
from unittest import mock

def test_get_usuario(client, mocker):
    usuario_mock = (1, "admin", "senha123", "administrador", 1)
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = usuario_mock
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.get('/usuarios/1')
    
    assert response.status_code == 200
    assert response.json['id_usuario'] == 1
    assert response.json['login'] == "admin"
    assert response.json['nivel_acesso'] == "administrador"
    assert response.json['id_professor'] == 1

def test_get_usuario_nao_encontrado(client, mocker):
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.get('/usuarios/999')
    
    assert response.status_code == 404
    assert "não encontrado" in response.json['error']

def test_add_usuario(client, mocker):
    novo_usuario = {
        "login": "professor1",
        "senha": "senha456",
        "nivel_acesso": "professor",
        "id_professor": 2
    }
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.post('/usuarios', json=novo_usuario)
    
    assert response.status_code == 201
    assert "Usuário adicionado" in response.json['message']

def test_update_usuario(client, mocker):
    usuario_atualizado = {
        "login": "admin_novo",
        "senha": "nova_senha",
        "nivel_acesso": "administrador",
        "id_professor": 1
    }
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.put('/usuarios/1', json=usuario_atualizado)
    
    assert response.status_code == 200
    assert "Usuario atualizado" in response.json['message']

def test_delete_usuario(client, mocker):
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.delete('/usuarios/1')
    
    assert response.status_code == 200
    assert "Usuario deletado" in response.json['message']

def test_add_usuario_login_duplicado(client, mocker):
    usuario_duplicado = {
        "login": "admin",
        "senha": "senha123",
        "nivel_acesso": "administrador",
        "id_professor": 1
    }
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Login já existe")
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.post('/usuarios', json=usuario_duplicado)
    
    assert response.status_code == 500
    assert "error" in response.json

def test_add_usuario_senha_vazia(client, mocker):
    usuario_senha_vazia = {
        "login": "novo_usuario",
        "senha": "",
        "nivel_acesso": "professor",
        "id_professor": 2
    }
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Senha não pode ser vazia")
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.post('/usuarios', json=usuario_senha_vazia)
    
    assert response.status_code == 500
    assert "error" in response.json