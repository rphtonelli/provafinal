from flask import Flask, request, jsonify
import Util.bd as bd

app = Flask(__name__)

@app.route('/usuarios', methods=['POST'])
def adicionar_usuario():
    data = request.get_json()
    
    required_fields = ['login', 'senha', 'nivel_acesso', 'id_professor']
    
    if not all([field in data for field in required_fields]):
        return jsonify({"error": "Campos obrigatórios não preenchidos"}), 400
    
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO usuario (login, senha, nivel_acesso, id_professor)
            VALUES (%s, %s, %s, %s)
            """,
            (data['login'], data['senha'], data['nivel_acesso'], data['id_professor'])
        )
        conn.commit()
        return jsonify({"message": "Usuário adicionado"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/usuarios/<int:id_usuario>', methods=['GET'])
def read_usuario(id_usuario):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM usuario WHERE id_usuario = %s
            """,
            (id_usuario,)
        )
        usuario = cursor.fetchone()
        if usuario is None:
            return jsonify({"error": "Usuário não encontrado"}), 404
        return jsonify({
            "id_usuario": usuario[0],
            "login": usuario[1],
            "senha": usuario[2],
            "nivel_acesso": usuario[3],
            "id_professor": usuario[4]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/usuarios/<int:id_usuario>', methods=['PUT'])
def update_usuario(id_usuario):
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE usuario
            SET login = %s, senha = %s, nivel_acesso = %s, id_professor = %s
            WHERE id_usuario = %s
            """,
            (data['login'], data['senha'], data['nivel_acesso'], data['id_professor'],
             id_usuario)
        )
        conn.commit()
        return jsonify({"message": "Usuario atualizado"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
def delete_usuario(id_usuario):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM usuario WHERE id_usuario = %s
            """,
            (id_usuario,)
        )
        conn.commit()
        return jsonify({"message": "Usuario deletado"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)