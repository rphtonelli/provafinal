from flask import Flask, request, jsonify
import Util.bd as bd
import base64

app = Flask(__name__)

@app.route('/atividade_aluno', methods=['POST'])
def adicionar_atividade_aluno():
    data = request.get_json()

    required_fields = ['id_aluno', 'id_atividade']

    if not all([field in data for field in required_fields]):
        return jsonify({"error": "Campos obrigatórios não preenchidos"}), 400
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        # Verificar se aluno existe
        cursor.execute("SELECT * FROM alunos WHERE id_aluno = %s", (data['id_aluno'],))
        aluno = cursor.fetchone()
        if aluno is None:
            return jsonify({"error": "Aluno não encontrado"}), 404

        # Verificar se atividade existe
        cursor.execute("SELECT * FROM atividade WHERE id_atividade = %s", (data['id_atividade'],))
        atividade = cursor.fetchone()
        if atividade is None:
            return jsonify({"error": "Atividade não encontrada"}), 404

        cursor.execute(
            """
            INSERT INTO atividade_aluno (id_atividade, id_aluno)
            VALUES (%s, %s)
            """,
            (data['id_atividade'], data['id_aluno'])
        )
        conn.commit()
        return jsonify({"message": "Atividade do aluno adicionada"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/atividade_aluno/<int:id_atividade>/<int:id_aluno>', methods=['GET'])
def read_atividade_aluno(id_atividade, id_aluno):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT aa.id_atividade, aa.id_aluno, at.descricao, at.data_realizacao, al.nome_completo
            FROM atividade_aluno aa
            JOIN atividade at ON aa.id_atividade = at.id_atividade
            JOIN alunos al ON aa.id_aluno = al.id_aluno
            WHERE aa.id_atividade = %s AND aa.id_aluno = %s
            """,
            (id_atividade, id_aluno)
        )
        atividade_aluno = cursor.fetchone()
        if atividade_aluno is None:
            return jsonify({"error": "Atividade do aluno não encontrada"}), 404
        return jsonify({
            "id_atividade": atividade_aluno[0],
            "id_aluno": atividade_aluno[1],
            "descricao_atividade": atividade_aluno[2],
            "data_realizacao": atividade_aluno[3],
            "nome_aluno": atividade_aluno[4]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/atividade_aluno/<int:id_atividade>/<int:id_aluno>', methods=['DELETE'])
def delete_atividade_aluno(id_atividade, id_aluno):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM atividade_aluno WHERE id_atividade = %s AND id_aluno = %s", 
            (id_atividade, id_aluno)
        )
        atividade_aluno = cursor.fetchone()

        if atividade_aluno is None:
            return jsonify({"error": "Atividade do aluno não encontrada"}), 404

        cursor.execute(
            "DELETE FROM atividade_aluno WHERE id_atividade = %s AND id_aluno = %s",
            (id_atividade, id_aluno)
        )
        conn.commit()
        return jsonify({"message": "Atividade do aluno atualizada"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/atividade_aluno/aluno/<int:id_aluno>', methods=['GET'])
def listar_atividades_aluno(id_aluno):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT aa.id_atividade, aa.id_aluno, at.descricao, at.data_realizacao
            FROM atividade_aluno aa
            JOIN atividade at ON aa.id_atividade = at.id_atividade
            WHERE aa.id_aluno = %s
            """,
            (id_aluno,)
        )
        atividades = cursor.fetchall()
        
        result = []
        for atividade in atividades:
            result.append({
                "id_atividade": atividade[0],
                "id_aluno": atividade[1],
                "descricao": atividade[2],
                "data_realizacao": atividade[3]
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)