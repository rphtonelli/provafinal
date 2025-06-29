"""
Módulo de gerenciamento de professores da escola infantil
Este módulo implementa as operações CRUD para a entidade Professor
"""
from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
import Util.bd as bd
from log_config import registrar_evento
from psycopg2 import Error

# Inicialização da aplicação Flask
app = Flask(__name__)

# Configuração do Swagger para documentação automática da API
swagger = Swagger(app, template={
    "info": {
        "title": "API de Gerenciamento de Professores",
        "description": "API RESTful para gerenciar professores da escola infantil",
        "version": "1.0.0"
    }
})

@app.route('/professores', methods=['POST'])
@swag_from({
    'tags': ['Professores'],
    'summary': 'Criar novo professor',
    'description': 'Cria um novo registro de professor no sistema',
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'id_professor': {'type': 'integer', 'example': 1},
                'nome_completo': {'type': 'string', 'example': 'Maria Santos'},
                'email': {'type': 'string', 'example': 'maria@escola.com'},
                'telefone': {'type': 'string', 'example': '11999999999'}
            },
            'required': ['id_professor', 'nome_completo']
        }
    }],
    'responses': {
        201: {'description': 'Professor criado com sucesso'},
        400: {'description': 'Erro na requisição'},
        500: {'description': 'Erro interno do servidor'}
    }
})
def create_professor():
    """
    Cria um novo professor no sistema
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
        # Executa INSERT para criar novo professor
        cursor.execute(
            """
            INSERT INTO professores (id_professor, nome_completo, email, telefone)
            VALUES (%s, %s, %s, %s)
            """,
            (data['id_professor'], data['nome_completo'], data.get('email'), data.get('telefone'))
        )
        conn.commit()  # Confirma a transação
        
        # Registra evento de sucesso no log
        registrar_evento("CREATE", mensagem=f"Professor {data['nome_completo']} criado com sucesso", sucesso=True)
        
        return jsonify({"message": "Professor criado com sucesso"}), 201
        
    except Error as e:
        conn.rollback()  # Desfaz a transação em caso de erro
        registrar_evento("CREATE", mensagem=f"Erro ao criar professor: {e}", sucesso=False)
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()  # Fecha cursor
        conn.close()    # Fecha conexão

@app.route('/professores/<int:id_professor>', methods=['GET'])
@swag_from({
    'tags': ['Professores'],
    'summary': 'Buscar professor por ID',
    'description': 'Retorna os dados de um professor específico',
    'parameters': [{
        'name': 'id_professor',
        'in': 'path',
        'type': 'integer',
        'required': True,
        'description': 'ID único do professor'
    }],
    'responses': {
        200: {'description': 'Professor encontrado'},
        404: {'description': 'Professor não encontrado'},
        500: {'description': 'Erro interno do servidor'}
    }
})
def read_professor(id_professor):
    """
    Busca um professor específico pelo ID
    Retorna todos os dados do professor encontrado
    """
    conn = bd.create_connection()
    
    if conn is None:
        registrar_evento("READ", mensagem="Falha na conexão com o banco de dados", sucesso=False)
        return jsonify({"error": "Failed to connect to the database"}), 500
    
    cursor = conn.cursor()
    try:
        # Busca professor pelo ID
        cursor.execute("SELECT * FROM professores WHERE id_professor = %s", (id_professor,))
        professor = cursor.fetchone()
        
        # Verifica se professor foi encontrado
        if professor is None:
            registrar_evento("READ", mensagem=f"Professor ID {id_professor} não encontrado", sucesso=False)
            return jsonify({"error": "Professor não encontrado"}), 404
        
        # Registra sucesso e retorna dados do professor
        registrar_evento("READ", mensagem=f"Professor {professor[1]} encontrado com sucesso", sucesso=True)
        
        return jsonify({
            "id_professor": professor[0],
            "nome_completo": professor[1],
            "email": professor[2],
            "telefone": professor[3]
        }), 200
        
    except Error as e:
        registrar_evento("READ", mensagem=f"Erro ao buscar professor: {e}", sucesso=False)
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/professores/<int:id_professor>', methods=['PUT'])
@swag_from({
    'tags': ['Professores'],
    'summary': 'Atualizar professor',
    'description': 'Atualiza os dados de um professor existente',
    'parameters': [{
        'name': 'id_professor',
        'in': 'path',
        'type': 'integer',
        'required': True,
        'description': 'ID único do professor'
    }, {
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'nome_completo': {'type': 'string'},
                'email': {'type': 'string'},
                'telefone': {'type': 'string'}
            }
        }
    }],
    'responses': {
        200: {'description': 'Professor atualizado com sucesso'},
        400: {'description': 'Erro na requisição'},
        500: {'description': 'Erro interno do servidor'}
    }
})
def update_professor(id_professor):
    """
    Atualiza os dados de um professor existente
    Recebe novos dados via JSON e atualiza no banco
    """
    data = request.get_json()
    conn = bd.create_connection()
    
    if conn is None:
        registrar_evento("UPDATE", mensagem="Falha na conexão com o banco de dados", sucesso=False)
        return jsonify({"error": "Failed to connect to the database"}), 500
    
    cursor = conn.cursor()
    try:
        # Atualiza dados do professor
        cursor.execute(
            """
            UPDATE professores
            SET nome_completo = %s, email = %s, telefone = %s
            WHERE id_professor = %s
            """,
            (data['nome_completo'], data.get('email'), data.get('telefone'), id_professor)
        )
        
        conn.commit()
        registrar_evento("UPDATE", mensagem=f"Professor ID {id_professor} atualizado com sucesso", sucesso=True)
        
        return jsonify({"message": "Professor atualizado com sucesso"}), 200
        
    except Error as e:
        conn.rollback()
        registrar_evento("UPDATE", mensagem=f"Erro ao atualizar professor: {e}", sucesso=False)
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/professores/<int:id_professor>', methods=['DELETE'])
@swag_from({
    'tags': ['Professores'],
    'summary': 'Deletar professor',
    'description': 'Remove um professor do sistema',
    'parameters': [{
        'name': 'id_professor',
        'in': 'path',
        'type': 'integer',
        'required': True,
        'description': 'ID único do professor'
    }],
    'responses': {
        200: {'description': 'Professor deletado com sucesso'},
        400: {'description': 'Erro na requisição'},
        500: {'description': 'Erro interno do servidor'}
    }
})
def delete_professor(id_professor):
    """
    Remove um professor do sistema
    Deleta o registro do banco de dados
    """
    conn = bd.create_connection()
    
    if conn is None:
        registrar_evento("DELETE", mensagem="Falha na conexão com o banco de dados", sucesso=False)
        return jsonify({"error": "Failed to connect to the database"}), 500
    
    cursor = conn.cursor()
    try:
        # Remove professor do banco
        cursor.execute("DELETE FROM professores WHERE id_professor = %s", (id_professor,))
        conn.commit()
        
        registrar_evento("DELETE", mensagem=f"Professor ID {id_professor} deletado com sucesso", sucesso=True)
        
        return jsonify({"message": "Professor deletado com sucesso"}), 200
        
    except Error as e:
        conn.rollback()
        registrar_evento("DELETE", mensagem=f"Erro ao deletar professor: {e}", sucesso=False)
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)