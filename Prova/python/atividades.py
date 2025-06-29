from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
import Util.bd as bd
from log_config import registrar_evento
import psycopg2
from psycopg2 import Error

# Inicialização da aplicação Flask
app = Flask(__name__)

# Configuração do Swagger para documentação automática da API
swagger = Swagger(app, template={
    "info": {
        "title": "API de Gerenciamento de Alunos",
        "description": "API RESTful para gerenciar alunos da escola infantil",
        "version": "1.0.0"
    }
})

@app.route('/alunos', methods=['POST'])
@swag_from({
    'tags': ['Alunos'],
    'summary': 'Criar novo aluno',
    'description': 'Cria um novo registro de aluno no sistema',
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'nome_completo': {'type': 'string', 'example': 'João Silva'},
                'data_nascimento': {'type': 'string', 'format': 'date', 'example': '2020-05-15'},
                'id_turma': {'type': 'integer', 'example': 1},
                'nome_responsavel': {'type': 'string', 'example': 'Maria Silva'},
                'telefone_responsavel': {'type': 'string', 'example': '11999999999'},
                'email_responsavel': {'type': 'string', 'example': 'maria@email.com'},
                'informacoes_adicionais': {'type': 'string', 'example': 'Alergia a amendoim'}
            },
            'required': ['nome_completo', 'data_nascimento', 'nome_responsavel', 'telefone_responsavel']
        }
    }],
    'responses': {
        201: {'description': 'Aluno criado com sucesso'},
        400: {'description': 'Erro na requisição'},
        500: {'description': 'Erro interno do servidor'}
    }
})
def create_aluno():
    """
    Cria um novo aluno no sistema
    Recebe dados via JSON e insere no banco de dados
    """
    data = request.get_json()  # Obtém dados JSON da requisição
    conn = bd.create_connection()  # Estabelece conexão com banco
    
    # Verifica se a conexão foi estabelecida
    if conn is None:
        registrar_evento("CREATE", mensagem="Falha na conexão com o banco de dados", sucesso=False)
        return jsonify({"error": "Failed to connect to the database"}), 500
    
    cursor = conn.cursor()
    try:
        # Executa INSERT para criar novo aluno
        cursor.execute(
            """
            INSERT INTO alunos (nome_completo, data_nascimento, id_turma, 
                              nome_responsavel, telefone_responsavel, 
                              email_responsavel, informacoes_adicionais)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_aluno
            """,
            (data['nome_completo'], data['data_nascimento'], data.get('id_turma'),
             data['nome_responsavel'], data['telefone_responsavel'], 
             data.get('email_responsavel'), data.get('informacoes_adicionais'))
        )
        
        # Obtém o ID do aluno criado
        aluno_id = cursor.fetchone()[0]
        conn.commit()  # Confirma a transação
        
        # Registra evento de sucesso no log
        registrar_evento("CREATE", aluno_id=aluno_id, aluno_nome=data['nome_completo'], 
                        sucesso=True, mensagem="Aluno criado com sucesso")
        
        return jsonify({"message": "Aluno criado com sucesso", "id_aluno": aluno_id}), 201
        
    except Error as e:
        conn.rollback()  # Desfaz a transação em caso de erro
        registrar_evento("CREATE", mensagem=f"Erro ao criar aluno: {e}", sucesso=False)
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()  # Fecha cursor
        conn.close()    # Fecha conexão

@app.route('/alunos/<int:id_aluno>', methods=['GET'])
@swag_from({
    'tags': ['Alunos'],
    'summary': 'Buscar aluno por ID',
    'description': 'Retorna os dados de um aluno específico',
    'parameters': [{
        'name': 'id_aluno',
        'in': 'path',
        'type': 'integer',
        'required': True,
        'description': 'ID único do aluno'
    }],
    'responses': {
        200: {'description': 'Aluno encontrado'},
        404: {'description': 'Aluno não encontrado'},
        500: {'description': 'Erro interno do servidor'}
    }
})
def read_aluno(id_aluno):
    """
    Busca um aluno específico pelo ID
    Retorna todos os dados do aluno encontrado
    """
    conn = bd.create_connection()
    
    if conn is None:
        registrar_evento("READ", aluno_id=id_aluno, sucesso=False, 
                        mensagem="Falha na conexão com o banco de dados")
        return jsonify({"error": "Failed to connect to the database"}), 500
    
    cursor = conn.cursor()
    try:
        # Busca aluno pelo ID
        cursor.execute("SELECT * FROM alunos WHERE id_aluno = %s", (id_aluno,))
        aluno = cursor.fetchone()
        
        # Verifica se aluno foi encontrado
        if aluno is None:
            registrar_evento("READ", aluno_id=id_aluno, sucesso=False, 
                           mensagem="Aluno não encontrado")
            return jsonify({"error": "Aluno não encontrado"}), 404
        
        # Registra sucesso e retorna dados do aluno
        registrar_evento("READ", aluno_id=id_aluno, aluno_nome=aluno[1], 
                        sucesso=True, mensagem="Aluno encontrado com sucesso")
        
        return jsonify({
            "id_aluno": aluno[0],
            "nome_completo": aluno[1],
            "data_nascimento": aluno[2].isoformat() if aluno[2] else None,
            "id_turma": aluno[3],
            "nome_responsavel": aluno[4],
            "telefone_responsavel": aluno[5],
            "email_responsavel": aluno[6],
            "informacoes_adicionais": aluno[7]
        }), 200
        
    except Error as e:
        registrar_evento("READ", aluno_id=id_aluno, sucesso=False, 
                        mensagem=f"Erro ao buscar aluno: {e}")
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/alunos/<int:id_aluno>', methods=['PUT'])
@swag_from({
    'tags': ['Alunos'],
    'summary': 'Atualizar aluno',
    'description': 'Atualiza os dados de um aluno existente',
    'parameters': [{
        'name': 'id_aluno',
        'in': 'path',
        'type': 'integer',
        'required': True,
        'description': 'ID único do aluno'
    }, {
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'nome_completo': {'type': 'string'},
                'data_nascimento': {'type': 'string', 'format': 'date'},
                'id_turma': {'type': 'integer'},
                'nome_responsavel': {'type': 'string'},
                'telefone_responsavel': {'type': 'string'},
                'email_responsavel': {'type': 'string'},
                'informacoes_adicionais': {'type': 'string'}
            }
        }
    }],
    'responses': {
        200: {'description': 'Aluno atualizado com sucesso'},
        400: {'description': 'Erro na requisição'},
        500: {'description': 'Erro interno do servidor'}
    }
})
def update_aluno(id_aluno):
    """
    Atualiza os dados de um aluno existente
    Recebe novos dados via JSON e atualiza no banco
    """
    data = request.get_json()
    conn = bd.create_connection()
    
    if conn is None:
        registrar_evento("UPDATE", aluno_id=id_aluno, sucesso=False, 
                        mensagem="Falha na conexão com o banco de dados")
        return jsonify({"error": "Failed to connect to the database"}), 500
    
    cursor = conn.cursor()
    try:
        # Atualiza dados do aluno
        cursor.execute(
            """
            UPDATE alunos 
            SET nome_completo = %s, data_nascimento = %s, id_turma = %s,
                nome_responsavel = %s, telefone_responsavel = %s,
                email_responsavel = %s, informacoes_adicionais = %s
            WHERE id_aluno = %s
            """,
            (data['nome_completo'], data['data_nascimento'], data.get('id_turma'),
             data['nome_responsavel'], data['telefone_responsavel'],
             data.get('email_responsavel'), data.get('informacoes_adicionais'), id_aluno)
        )
        
        conn.commit()
        registrar_evento("UPDATE", aluno_id=id_aluno, aluno_nome=data['nome_completo'],
                        sucesso=True, mensagem="Aluno atualizado com sucesso")
        
        return jsonify({"message": "Aluno atualizado com sucesso"}), 200
        
    except Error as e:
        conn.rollback()
        registrar_evento("UPDATE", aluno_id=id_aluno, sucesso=False, 
                        mensagem=f"Erro ao atualizar aluno: {e}")
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/alunos/<int:id_aluno>', methods=['DELETE'])
@swag_from({
    'tags': ['Alunos'],
    'summary': 'Deletar aluno',
    'description': 'Remove um aluno do sistema',
    'parameters': [{
        'name': 'id_aluno',
        'in': 'path',
        'type': 'integer',
        'required': True,
        'description': 'ID único do aluno'
    }],
    'responses': {
        200: {'description': 'Aluno deletado com sucesso'},
        400: {'description': 'Erro na requisição'},
        500: {'description': 'Erro interno do servidor'}
    }
})
def delete_aluno(id_aluno):
    """
    Remove um aluno do sistema
    Deleta o registro do banco de dados
    """
    conn = bd.create_connection()
    
    if conn is None:
        registrar_evento("DELETE", aluno_id=id_aluno, sucesso=False, 
                        mensagem="Falha na conexão com o banco de dados")
        return jsonify({"error": "Failed to connect to the database"}), 500
    
    cursor = conn.cursor()
    try:
        # Remove aluno do banco
        cursor.execute("DELETE FROM alunos WHERE id_aluno = %s", (id_aluno,))
        conn.commit()
        
        registrar_evento("DELETE", aluno_id=id_aluno, sucesso=True, 
                        mensagem="Aluno deletado com sucesso")
        
        return jsonify({"message": "Aluno deletado com sucesso"}), 200
        
    except Error as e:
        conn.rollback()
        registrar_evento("DELETE", aluno_id=id_aluno, sucesso=False, 
                        mensagem=f"Erro ao deletar aluno: {e}")
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)