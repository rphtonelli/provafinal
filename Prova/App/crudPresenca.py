from flask import Flask, request, jsonify
import Util.bd as bd
import base64

app = Flask(__name__)

@app.route('/presencas', methods=['POST'])
def adicionar_presenca():
    data = request.get_json()

    required_fields = ['id_aluno', 'data_presenca', 'presente']

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
            INSERT INTO presenca (id_aluno, data_presenca, presente)
            VALUES (%s, %s, %s)
            """,
            (data['id_aluno'], data['data_presenca'], data['presente'])
        )
        conn.commit()
        return jsonify({"message": "Presença adicionada"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/presencas/<int:id_presenca>', methods=['GET'])
def read_presenca(id_presenca):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM presenca WHERE id_presenca = %s
            """,
            (id_presenca,)
        )
        presenca = cursor.fetchone()
        if presenca is None:
            return jsonify({"error": "Presença não encontrada"}), 404
        return jsonify({
            "id_presenca": presenca[0],
            "id_aluno": presenca[1],
            "data_presenca": presenca[2],
            "presente": presenca[3],
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/presencas/<int:id_presenca>', methods=['PUT'])
def update_presenca(id_presenca):
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE presenca SET id_aluno = %s, data_presenca = %s, presente = %s
            WHERE id_presenca = %s
            """,
            (data['id_aluno'], data['data_presenca'], data['presente'], id_presenca)
        )
        conn.commit()
        return jsonify({"message": "Presença atualizada"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/presencas/<int:id_presenca>', methods=['DELETE'])
def delete_presenca(id_presenca):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM presenca WHERE id_presenca = %s
            """,
            (id_presenca,)
        )
        conn.commit()
        return jsonify({"message": "Presença deletada"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)