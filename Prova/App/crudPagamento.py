from flask import Flask, request, jsonify
import Util.bd as bd

app = Flask(__name__)

@app.route('/pagamentos', methods=['POST'])
def adicionar_pagamento():
    data = request.get_json()

    required_fields = ['id_aluno', 'valor_pago', 'data_pagamento', 'forma_pagamento']

    if not all([field in data for field in required_fields]):
        return jsonify({"error": "Campos obrigatórios não preenchidos"}), 400
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM alunos WHERE id_aluno = %s", (data['id_aluno'],))
        aluno = cursor.fetchone()

        if aluno is None:
            return jsonify({"error": "Aluno não encontrado"}), 404

        cursor.execute(
            """
            INSERT INTO pagamento (id_aluno, data_pagamento, valor_pago, forma_pagamento, referencia, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (data['id_aluno'], data['data_pagamento'], data['valor_pago'], data['forma_pagamento'], data.get('referencia', ''), data.get('status', 'pendente'))
        )
        conn.commit()
        return jsonify({"message": "Pagamento adicionado"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
@app.route('/pagamentos/<int:id_pagamento>', methods=['GET'])
def read_pagamento(id_pagamento):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM pagamento WHERE id_pagamento = %s
            """,
            (id_pagamento,)
        )
        pagamento = cursor.fetchone()
        if pagamento is None:
            return jsonify({"error": "Pagamento não encontrado"}), 404
        return jsonify({
            "id_pagamento": pagamento[0],
            "id_aluno": pagamento[1],
            "data_pagamento": pagamento[2],
            "valor_pago": pagamento[3],
            "forma_pagamento": pagamento[4],
            "referencia": pagamento[5],
            "status": pagamento[6],
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/pagamentos/<int:id_pagamento>', methods=['PUT'])
def update_pagamento(id_pagamento):
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE pagamento
            SET id_aluno = %s, data_pagamento = %s, valor_pago = %s, forma_pagamento = %s, referencia = %s, status = %s
            WHERE id_pagamento = %s
            """,
            (data['id_aluno'], data['data_pagamento'], data['valor_pago'], data['forma_pagamento'], data['referencia'], data['status'], id_pagamento)
        )
        conn.commit()
        return jsonify({"message": "Pagamento atualizado"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Método para deletar um pagamento
@app.route('/pagamentos/<int:id_pagamento>', methods=['DELETE'])
def delete_pagamento(id_pagamento):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM pagamento WHERE id_pagamento = %s
            """,
            (id_pagamento,)
        )
        conn.commit()
        return jsonify({"message": "Pagamento deletado"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)