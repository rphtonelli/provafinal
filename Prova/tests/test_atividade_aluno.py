import pytest
from unittest import mock

def test_get_atividade_aluno(client, mocker):
    atividade_aluno_mock = (1, 123, 1, "2023-06-01", "exercicio", "Lista resolvida", "Bem feito")
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = atividade_aluno_mock
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.get('/atividade_aluno/1')
    
    assert response.status_code == 200
    assert response.json['id_atividade_aluno'] == 1
    assert response.json['id_aluno'] == 123
    assert response.json['id_atividade'] == 1
    assert response.json['tipo_atividade'] == "exercicio"

def test_get_atividade_aluno_nao_encontrada(client, mocker):
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.get('/atividade_aluno/999')
    
    assert response.status_code == 404
    assert "não encontrada" in response.json['error']

def test_add_atividade_aluno(client, mocker):
    nova_atividade_aluno = {
        "id_aluno": 123,
        "id_atividade": 1,
        "data_atividade": "2023-06-01",
        "tipo_atividade": "exercicio",
        "descricao_atividade": "Lista de exercícios resolvida",
        "observacoes_atividade": "Entregue no prazo"
    }
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    # Mock para encontrar o aluno
    mock_cursor.fetchone.return_value = (123, "João Silva")
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.post('/atividade_aluno', json=nova_atividade_aluno)
    
    assert response.status_code == 201
    assert "Atividade do aluno adicionada" in response.json['message']

def test_add_atividade_aluno_campos_obrigatorios(client):
    atividade_aluno_incompleta = {
        "id_aluno": 123,
        "id_atividade": 1
        # Faltando outros campos obrigatórios
    }
    
    response = client.post('/atividade_aluno', json=atividade_aluno_incompleta)
    
    assert response.status_code == 400
    assert "Campos obrigatórios" in response.json['error']

def test_add_atividade_aluno_nao_encontrado(client, mocker):
    nova_atividade_aluno = {
        "id_aluno": 999,
        "id_atividade": 1,
        "data_atividade": "2023-06-01",
        "tipo_atividade": "exercicio",
        "descricao_atividade": "Lista de exercícios",
        "observacoes_atividade": "Para casa"
    }
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    # Mock para não encontrar o aluno
    mock_cursor.fetchone.return_value = None
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.post('/atividade_aluno', json=nova_atividade_aluno)
    
    assert response.status_code == 404
    assert "Aluno não encontrado" in response.json['error']

def test_update_atividade_aluno(client, mocker):
    atividade_aluno_atualizada = {
        "id_aluno": 123,
        "id_atividade": 1,
        "data_atividade": "2023-06-02",
        "tipo_atividade": "prova",
        "descricao_atividade": "Prova corrigida",
        "observacoes_atividade": "Nota 8.5"
    }
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    # Mock para encontrar a atividade do aluno
    mock_cursor.fetchone.return_value = (1, 123, 1, "2023-06-01", "exercicio", "Lista", "OK")
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.put('/atividade_aluno/1', json=atividade_aluno_atualizada)
    
    assert response.status_code == 200
    assert "Atividade do aluno atualizada" in response.json['message']

def test_update_atividade_aluno_nao_encontrada(client, mocker):
    atividade_aluno_atualizada = {
        "id_aluno": 123,
        "id_atividade": 1,
        "data_atividade": "2023-06-02",
        "tipo_atividade": "prova",
        "descricao_atividade": "Prova corrigida",
        "observacoes_atividade": "Nota 8.5"
    }
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    # Mock para não encontrar a atividade do aluno
    mock_cursor.fetchone.return_value = None
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.put('/atividade_aluno/999', json=atividade_aluno_atualizada)
    
    assert response.status_code == 404
    assert "não encontrada" in response.json['error']

def test_delete_atividade_aluno(client, mocker):
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    # Mock para encontrar a atividade do aluno
    mock_cursor.fetchone.return_value = (1, 123, 1, "2023-06-01", "exercicio", "Lista", "OK")
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.delete('/atividade_aluno/1')
    
    assert response.status_code == 200
    assert "Atividade do aluno deletada" in response.json['message']

def test_delete_atividade_aluno_nao_encontrada(client, mocker):
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    # Mock para não encontrar a atividade do aluno
    mock_cursor.fetchone.return_value = None
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.delete('/atividade_aluno/999')
    
    assert response.status_code == 404
    assert "não encontrada" in response.json['error']