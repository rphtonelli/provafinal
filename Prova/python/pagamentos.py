from flask import Flask, request, jsonify
import Util.bd as bd
import base64

app = Flask(__name__)

@app.route('/pagamentos', methods=['POST'])
def create_pagamento():
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO pagamentos (id_aluno, data_pagamento, valor_pago, forma_pagamento, referencia)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (data['id_aluno'], data['data_pagamento'], data['valor_pago'], data['forma_pagamento'], data['referencia'])
        )
        conn.commit()
        return jsonify({"message": "Pagamento criado com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/pagamentos/<int:id_pagamento>', methods=['GET'])
def read_pagamento(id_pagamento):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM pagamentos WHERE id_pagamento = %s", (id_pagamento,))
        pagamento = cursor.fetchone()
        if pagamento is None:
            return jsonify({"error": "Pagamento não encontrado"}), 404
        return jsonify({
            "id_pagamento": pagamento[0],
            "id_aluno": pagamento[1],
            "data_pagamento": pagamento[2],
            "valor_pago": pagamento[3],
            "forma_pagamento": pagamento[4],
            "referencia": pagamento[5]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/pagamentos/<int:id_pagamento>', methods=['PUT'])
def update_pagamento(id_pagamento):
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE pagamentos
            SET id_aluno = %s, data_pagamento = %s, valor_pago = %s, 
                forma_pagamento = %s, referencia = %s
            WHERE id_pagamento = %s
            """,
            (data['id_aluno'], data['data_pagamento'], data['valor_pago'], 
             data['forma_pagamento'], data['referencia'], id_pagamento)
        )
        conn.commit()
        return jsonify({"message": "Pagamento atualizado com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/pagamentos/<int:id_pagamento>', methods=['DELETE'])
def delete_pagamento(id_pagamento):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM pagamentos WHERE id_pagamento = %s", (id_pagamento,))
        conn.commit()
        return jsonify({"message": "Pagamento deletado com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)