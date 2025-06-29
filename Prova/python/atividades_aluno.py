from flask import Flask, request, jsonify
import Util.bd as bd
import base64

app = Flask(__name__)

@app.route('/atividade_aluno', methods=['POST'])
def create_atividade_aluno():
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO atividade_aluno (id_atividade, id_aluno)
            VALUES (%s, %s)
            """,
            (data['id_atividade'], data['id_aluno'])
        )
        conn.commit()
        return jsonify({"message": "Relação Atividade-Aluno criada com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/atividade_aluno/<int:id_atividade>/<int:id_aluno>', methods=['GET'])
def read_atividade_aluno(id_atividade, id_aluno):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM atividade_aluno WHERE id_atividade = %s AND id_aluno = %s",
            (id_atividade, id_aluno)
        )
        relacao = cursor.fetchone()
        if relacao is None:
            return jsonify({"error": "Relação Atividade-Aluno não encontrada"}), 404
        return jsonify({
            "id_atividade": relacao[0],
            "id_aluno": relacao[1]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/atividade_aluno/<int:id_atividade>/<int:id_aluno>', methods=['DELETE'])
def delete_atividade_aluno(id_atividade, id_aluno):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM atividade_aluno WHERE id_atividade = %s AND id_aluno = %s",
            (id_atividade, id_aluno)
        )
        conn.commit()
        return jsonify({"message": "Relação Atividade-Aluno deletada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)