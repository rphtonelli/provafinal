import pytest
from unittest import mock

def test_get_aluno(client, mocker):
    aluno_mock = (1, "João da Silva", "2000-01-01", 1, "Maria Silva", "11999999999", "maria@email.com", "Informações adicionais")
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = aluno_mock
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.get('/alunos/1')
    
    assert response.status_code == 200
    assert response.json['id_aluno'] == 1
    assert response.json['nome_completo'] == 'João da Silva'
    assert response.json['data_nascimento'] == '2000-01-01'
    assert response.json['id_turma'] == 1

def test_get_aluno_nao_encontrado(client, mocker):
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.get('/alunos/999')
    
    assert response.status_code == 404
    assert "não encontrado" in response.json['error']

def test_add_aluno(client, mocker):
    novo_aluno = {
        "nome_completo": "Maria Oliveira",
        "data_nascimento": "2001-05-15",
        "id_turma": 1,
        "nome_responsavel": "José Oliveira",
        "telefone_responsavel": "11888888888",
        "email_responsavel": "jose@email.com",
        "informacoes_adicionais": "Aluna dedicada"
    }
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (1, "Turma A", 1, "08:00-12:00")  # Mock da turma existente
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.post('/alunos', json=novo_aluno)
    
    assert response.status_code == 201
    assert "Aluno adicionado" in response.json['message']

def test_add_aluno_campos_obrigatorios(client, mocker):
    aluno_incompleto = {
        "nome_completo": "Maria Oliveira"
        # Faltando campos obrigatórios
    }
    
    response = client.post('/alunos', json=aluno_incompleto)
    
    assert response.status_code == 400
    assert "Campos obrigatórios" in response.json['error']

def test_update_aluno(client, mocker):
    aluno_atualizado = {
        "nome_completo": "João da Silva Jr.",
        "data_nascimento": "2000-01-01",
        "id_turma": 2,
        "nome_responsavel": "Maria Silva Jr.",
        "telefone_responsavel": "11777777777",
        "email_responsavel": "maria.jr@email.com",
        "informacoes_adicionais": "Atualizado"
    }
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.put('/alunos/1', json=aluno_atualizado)
    
    assert response.status_code == 200
    assert "Aluno atualizado" in response.json['message']

def test_delete_aluno(client, mocker):
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.delete('/alunos/1')
    
    assert response.status_code == 200
    assert "Aluno deletado" in response.json['message']