from flask import Flask, request, jsonify
import Util.bd as bd
import base64

app = Flask(__name__)

@app.route('/atividade', methods=['POST'])
def adicionar_atividade():
    data = request.get_json()

    required_fields = ['descricao', 'data_realizacao']

    if not all([field in data for field in required_fields]):
        return jsonify({"error": "Campos obrigatórios não preenchidos"}), 400
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO atividade (descricao, data_realizacao)
            VALUES (%s, %s)
            """,
            (data['descricao'], data['data_realizacao'])
        )
        conn.commit()
        return jsonify({"message": "Atividade adicionada"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/atividade/<int:id_atividade>', methods=['GET'])
def read_atividade(id_atividade):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM atividade WHERE id_atividade = %s
            """,
            (id_atividade,)
        )
        atividade = cursor.fetchone()
        if atividade is None:
            return jsonify({"error": "Atividade não encontrada"}), 404
        return jsonify({
            "id_atividade": atividade[0],
            "descricao": atividade[1],
            "data_realizacao": atividade[2]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/atividade/<int:id_atividade>', methods=['PUT'])
def update_atividade(id_atividade):
    data = request.get_json()

    required_fields = ['descricao', 'data_realizacao']

    if not all([field in data for field in required_fields]):
        return jsonify({"error": "Campos obrigatórios não preenchidos"}), 400

    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500

    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE atividade
            SET descricao = %s, data_realizacao = %s
            WHERE id_atividade = %s
            """,
            (data['descricao'], data['data_realizacao'], id_atividade)
        )
        conn.commit()
        return jsonify({"message": "Atividade atualizada"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/atividade/<int:id_atividade>', methods=['DELETE'])
def delete_atividade(id_atividade):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500

    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM atividade WHERE id_atividade = %s
            """,
            (id_atividade,)
        )
        conn.commit()
        return jsonify({"message": "Atividade deletada"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)