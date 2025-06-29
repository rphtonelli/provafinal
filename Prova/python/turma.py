"""
Módulo de gerenciamento de turmas da escola infantil
Este módulo implementa as operações CRUD para a entidade Turma
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
        "title": "API de Gerenciamento de Turmas",
        "description": "API RESTful para gerenciar turmas da escola infantil",
        "version": "1.0.0"
    }
})

@app.route('/turmas', methods=['POST'])
@swag_from({
    'tags': ['Turmas'],
    'summary': 'Criar nova turma',
    'description': 'Cria um novo registro de turma no sistema',
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'id_turma': {'type': 'integer', 'example': 1},
                'nome_turma': {'type': 'string', 'example': 'Turma A - Manhã'},
                'id_professor': {'type': 'integer', 'example': 1},
                'horario': {'type': 'string', 'example': '08:00 - 12:00'}
            },
            'required': ['id_turma', 'nome_turma']
        }
    }],
    'responses': {
        201: {'description': 'Turma criada com sucesso'},
        400: {'description': 'Erro na requisição'},
        500: {'description': 'Erro interno do servidor'}
    }
})
def create_turma():
    """
    Cria uma nova turma no sistema
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
        # Executa INSERT para criar nova turma
        cursor.execute(
            """
            INSERT INTO turmas (id_turma, nome_turma, id_professor, horario)
            VALUES (%s, %s, %s, %s)
            """,
            (data['id_turma'], data['nome_turma'], data.get('id_professor'), data.get('horario'))
        )
        conn.commit()  # Confirma a transação
        
        # Registra evento de sucesso no log
        registrar_evento("CREATE", mensagem=f"Turma {data['nome_turma']} criada com sucesso", sucesso=True)
        
        return jsonify({"message": "Turma criada com sucesso"}), 201
        
    except Error as e:
        conn.rollback()  # Desfaz a transação em caso de erro
        registrar_evento("CREATE", mensagem=f"Erro ao criar turma: {e}", sucesso=False)
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()  # Fecha cursor
        conn.close()    # Fecha conexão

@app.route('/turmas/<int:id_turma>', methods=['GET'])
def read_turma(id_turma):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM turmas WHERE id_turma = %s", (id_turma,))
        turma = cursor.fetchone()
        if turma is None:
            return jsonify({"error": "Turma não encontrada"}), 404
        return jsonify({
            "id_turma": turma[0],
            "nome_turma": turma[1],
            "id_professor": turma[2],
            "horario": turma[3]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/turmas/<int:id_turma>', methods=['PUT'])
def update_turma(id_turma):
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE turmas
            SET nome_turma = %s, id_professor = %s, horario = %s
            WHERE id_turma = %s
            """,
            (data['nome_turma'], data['id_professor'], data['horario'], id_turma)
        )
        conn.commit()
        return jsonify({"message": "Turma atualizada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/turmas/<int:id_turma>', methods=['DELETE'])
def delete_turma(id_turma):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM turmas WHERE id_turma = %s", (id_turma,))
        conn.commit()
        return jsonify({"message": "Turma deletada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)