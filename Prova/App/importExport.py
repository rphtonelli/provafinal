from flask import Flask, request, jsonify, send_file, Blueprint
import Util.bd as bd
import csv
import json
import io
from datetime import datetime
import pandas as pd

import_export_bp = Blueprint('import_export', __name__)

# IMPORTAÇÃO DE ALUNOS
@import_export_bp.route('/alunos/import', methods=['POST'])
def import_alunos():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Arquivo vazio"}), 400
    
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha na conexão com BD"}), 500
    
    cursor = conn.cursor()
    sucessos = 0
    erros = []
    
    try:
        # Ler CSV
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.DictReader(stream)
        
        for row_num, row in enumerate(csv_input, start=2):
            try:
                cursor.execute("""
                    INSERT INTO alunos (nome_completo, data_nascimento, nome_responsavel, 
                    telefone_responsavel, email_responsavel, informacoes_adicionais)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    row['nome_completo'], row['data_nascimento'], row['nome_responsavel'],
                    row['telefone_responsavel'], row['email_responsavel'], 
                    row.get('informacoes_adicionais', '')
                ))
                sucessos += 1
            except Exception as e:
                erros.append(f"Linha {row_num}: {str(e)}")
        
        conn.commit()
        return jsonify({
            "message": f"Importação concluída: {sucessos} sucessos, {len(erros)} erros",
            "sucessos": sucessos,
            "erros": erros
        }), 200
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Erro na importação: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

# EXPORTAÇÃO DE ALUNOS
@import_export_bp.route('/alunos/export', methods=['GET'])
def export_alunos():
    formato = request.args.get('formato', 'csv')
    
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha na conexão com BD"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM alunos")
        alunos = cursor.fetchall()
        
        if formato == 'csv':
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Cabeçalho
            writer.writerow(['id_aluno', 'nome_completo', 'data_nascimento', 
                           'nome_responsavel', 'telefone_responsavel', 'email_responsavel', 
                           'informacoes_adicionais'])
            
            # Dados
            for aluno in alunos:
                writer.writerow(aluno)
            
            output.seek(0)
            return send_file(
                io.BytesIO(output.getvalue().encode('utf-8')),
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'alunos_{datetime.now().strftime("%Y%m%d")}.csv'
            )
            
        elif formato == 'json':
            alunos_dict = []
            for aluno in alunos:
                alunos_dict.append({
                    'id_aluno': aluno[0],
                    'nome_completo': aluno[1],
                    'data_nascimento': str(aluno[2]),
                    'nome_responsavel': aluno[3],
                    'telefone_responsavel': aluno[4],
                    'email_responsavel': aluno[5],
                    'informacoes_adicionais': aluno[6]
                })
            
            return send_file(
                io.BytesIO(json.dumps(alunos_dict, indent=2).encode('utf-8')),
                mimetype='application/json',
                as_attachment=True,
                download_name=f'alunos_{datetime.now().strftime("%Y%m%d")}.json'
            )
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# EXPORTAÇÃO DE RELATÓRIO DE PAGAMENTOS
@import_export_bp.route('/pagamentos/export', methods=['GET'])
def export_pagamentos():
    mes = request.args.get('mes')
    ano = request.args.get('ano')
    formato = request.args.get('formato', 'csv')
    
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha na conexão com BD"}), 500
    
    cursor = conn.cursor()
    try:
        query = """
            SELECT p.id_pagamento, a.nome_completo, p.data_pagamento, 
                   p.valor_pago, p.forma_pagamento, p.status
            FROM pagamento p
            JOIN alunos a ON p.id_aluno = a.id_aluno
        """
        params = []
        
        if mes and ano:
            query += " WHERE EXTRACT(MONTH FROM p.data_pagamento) = %s AND EXTRACT(YEAR FROM p.data_pagamento) = %s"
            params = [mes, ano]
        
        cursor.execute(query, params)
        pagamentos = cursor.fetchall()
        
        if formato == 'csv':
            output = io.StringIO()
            writer = csv.writer(output)
            
            writer.writerow(['ID', 'Aluno', 'Data', 'Valor', 'Forma Pagamento', 'Status'])
            
            for pag in pagamentos:
                writer.writerow(pag)
            
            output.seek(0)
            filename = f'pagamentos_{mes}_{ano}.csv' if mes and ano else f'pagamentos_{datetime.now().strftime("%Y%m%d")}.csv'
            
            return send_file(
                io.BytesIO(output.getvalue().encode('utf-8')),
                mimetype='text/csv',
                as_attachment=True,
                download_name=filename
            )
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# IMPORTAÇÃO DE PROFESSORES
@import_export_bp.route('/professores/import', methods=['POST'])
def import_professores():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400
    
    file = request.files['file']
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha na conexão com BD"}), 500
    
    cursor = conn.cursor()
    sucessos = 0
    erros = []
    
    try:
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.DictReader(stream)
        
        for row_num, row in enumerate(csv_input, start=2):
            try:
                cursor.execute("""
                    INSERT INTO professor (nome_completo, email, telefone)
                    VALUES (%s, %s, %s)
                """, (row['nome_completo'], row['email'], row['telefone']))
                sucessos += 1
            except Exception as e:
                erros.append(f"Linha {row_num}: {str(e)}")
        
        conn.commit()
        return jsonify({
            "message": f"Importação concluída: {sucessos} sucessos, {len(erros)} erros",
            "sucessos": sucessos,
            "erros": erros
        }), 200
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Erro na importação: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()