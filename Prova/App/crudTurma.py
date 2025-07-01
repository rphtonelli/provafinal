from flask import Flask, request, jsonify
import Util.bd as bd
import base64

app = Flask(__name__)

@app.route('/turmas', methods=['POST'])
def adicionar_turma():
    data = request.get_json()
    
    required_fields = ['nome_completo', 'nome_turma', 'horario']
    
    if not all([field in data for field in required_fields]):
        return jsonify({"error": "Campos obrigatórios não preenchidos"}), 400
    
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_professor FROM professor WHERE nome_completo = %s", (data['nome_completo'],))
        professor = cursor.fetchone()
        
        if professor is None:
            return jsonify({"error": "Professor não encontrado"}), 404
        
        id_professor = professor[0]
        
        cursor.execute(
            """
            INSERT INTO turma (nome_turma, id_professor, horario)
            VALUES (%s, %s, %s)
            """,
            (data['nome_turma'], id_professor, data['horario'])
        )
        conn.commit()
        return jsonify({"message": "Turma adicionada com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
        
@app.route('/turmas/<int:id_turma>', methods=['GET'])
def read_turma(id_turma):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM turma WHERE id_turma = %s
            """,
            (id_turma,)
        )
        turma = cursor.fetchone()
        if turma is None:
            return jsonify({"error": "Turma não encontrada"}), 404
        return jsonify({
            "id_turma": turma[0],
            "nome_turma": turma[1],
            "id_professor": turma[2],
            "horario": turma[3],
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/turmas/<int:id_turma>', methods=['PUT'])
def update_turma(id_turma):
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE turma
            SET nome_turma = %s, id_professor = %s, horario = %s
            WHERE id_turma = %s
            """,
            (data['nome_turma'], data['id_professor'],
             data['horario'], id_turma)
        )
        conn.commit()
        return jsonify({"message": "Turma atualizada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/turmas/<int:id_turma>', methods=['DELETE'])
def delete_turma(id_turma):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM turma WHERE id_turma = %s
            """,
            (id_turma,)
        )
        conn.commit()
        return jsonify({"message": "Turma deletada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)