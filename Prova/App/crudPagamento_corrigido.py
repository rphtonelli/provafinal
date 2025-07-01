from flask import Flask, request, jsonify, Blueprint
import Util.bd as bd
import base64
import logging

logging.basicConfig(
    filename='escola_infantil.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

pagamento_bp = Blueprint('pagamento', __name__)

@pagamento_bp.route('/pagamentos', methods=['POST'])
def adicionar_pagamento():
    data = request.get_json()  # Corrigido de request.get.json()

    required_fields = ['id_aluno', 'valor', 'data_pagamento', 'metodo_pagamento']

    if not all([field in data for field in required_fields]):
        logging.warning(f"CREATE: Campos obrigatórios ausentes em pagamento")
        return jsonify({"error": "Campos obrigatórios não preenchidos"}), 400
    
    conn = bd.create_connection()
    if conn is None:
        logging.error("CREATE: Falha ao conectar ao banco de dados.")
        return jsonify({"error": "Connection to DB failed"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM alunos WHERE id_aluno = %s", (data['id_aluno'],))
        aluno = cursor.fetchone()

        if aluno is None:
            logging.warning(f"CREATE: Aluno com ID {data['id_aluno']} não encontrado.")
            return jsonify({"error": "Aluno não encontrado"}), 404

        cursor.execute(
            """
            INSERT INTO pagamentos (id_aluno, valor, data_pagamento, metodo_pagamento)
            VALUES (%s, %s, %s, %s)
            RETURNING id_pagamento
            """,
            (data['id_aluno'], data['valor'], data['data_pagamento'], data['metodo_pagamento'])
        )
        id_pagamento = cursor.fetchone()[0]
        conn.commit()
        logging.info(f"CREATE: Pagamento para aluno {data['id_aluno']} inserido com sucesso. ID gerado: {id_pagamento}")
        return jsonify({"message": "Pagamento adicionado", "id_pagamento": id_pagamento}), 201
    except Exception as e:
        conn.rollback()
        logging.error(f"CREATE: Erro ao inserir pagamento - {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@pagamento_bp.route('/pagamentos/<int:id_pagamento>', methods=['GET'])
def read_pagamento(id_pagamento):
    conn = bd.create_connection()
    if conn is None:
        logging.error("READ: Falha ao conectar ao banco de dados.")
        return jsonify({"error": "Connection to DB failed"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM pagamentos WHERE id_pagamento = %s
            """,
            (id_pagamento,)
        )
        pagamento = cursor.fetchone()
        if pagamento is None:
            logging.warning(f"READ: Pagamento com ID {id_pagamento} não encontrado.")
            return jsonify({"error": "Pagamento não encontrado"}), 404
        
        logging.info(f"READ: Pagamento com ID {id_pagamento} consultado com sucesso.")
        return jsonify({
            "id_pagamento": pagamento[0],
            "id_aluno": pagamento[1],
            "data_pagamento": pagamento[2],
            "valor": pagamento[3],  # Corrigido para manter consistência com o INSERT
            "metodo_pagamento": pagamento[4],  # Corrigido para manter consistência com o INSERT
            "referencia": pagamento[5],
            "status": pagamento[6],
        }), 200
    except Exception as e:
        logging.error(f"READ: Erro ao consultar pagamento com ID {id_pagamento} - {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@pagamento_bp.route('/pagamentos/<int:id_pagamento>', methods=['PUT'])
def update_pagamento(id_pagamento):
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        logging.error("UPDATE: Falha ao conectar ao banco de dados.")
        return jsonify({"error": "Connection to DB failed"}), 500
    
    cursor = conn.cursor()
    try:
        # Verificar se o pagamento existe
        cursor.execute("SELECT * FROM pagamentos WHERE id_pagamento = %s", (id_pagamento,))
        if cursor.fetchone() is None:
            logging.warning(f"UPDATE: Pagamento com ID {id_pagamento} não encontrado.")
            return jsonify({"error": "Pagamento não encontrado"}), 404
            
        cursor.execute(
            """
            UPDATE pagamentos
            SET id_aluno = %s, data_pagamento = %s, valor = %s, metodo_pagamento = %s, referencia = %s, status = %s
            WHERE id_pagamento = %s
            """,
            (data['id_aluno'], data['data_pagamento'], data['valor'], data['metodo_pagamento'], 
             data.get('referencia', ''), data.get('status', 'pendente'), id_pagamento)
        )
        conn.commit()
        logging.info(f"UPDATE: Pagamento com ID {id_pagamento} atualizado com sucesso.")
        return jsonify({"message": "Pagamento atualizado"}), 200
    except Exception as e:
        conn.rollback()
        logging.error(f"UPDATE: Erro ao atualizar pagamento com ID {id_pagamento} - {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@pagamento_bp.route('/pagamentos/<int:id_pagamento>', methods=['DELETE'])
def delete_pagamento(id_pagamento):
    conn = bd.create_connection()
    if conn is None:
        logging.error("DELETE: Falha ao conectar ao banco de dados.")
        return jsonify({"error": "Connection to DB failed"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM pagamentos WHERE id_pagamento = %s", (id_pagamento,))
        if cursor.fetchone() is None:
            logging.warning(f"DELETE: Pagamento com ID {id_pagamento} não encontrado.")
            return jsonify({"error": "Pagamento não encontrado"}), 404
            
        cursor.execute(
            """
            DELETE FROM pagamentos WHERE id_pagamento = %s
            """,
            (id_pagamento,)
        )
        conn.commit()
        logging.info(f"DELETE: Pagamento com ID {id_pagamento} removido com sucesso.")
        return jsonify({"message": "Pagamento deletado"}), 200
    except Exception as e:
        conn.rollback()
        logging.error(f"DELETE: Erro ao deletar pagamento com ID {id_pagamento} - {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Não é necessário o bloco app.run quando usando Blueprint