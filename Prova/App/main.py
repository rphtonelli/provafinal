# main.py
from flask import Flask

app = Flask(__name__)

# Importando as rotas dos módulos
try:
    from crudAlunos import app as alunos_app
    for rule in alunos_app.url_map.iter_rules():
        if rule.endpoint != 'static':
            app.add_url_rule(rule.rule, rule.endpoint, alunos_app.view_functions[rule.endpoint], methods=rule.methods)
except ImportError:
    print("Módulo crudAlunos não encontrado")

try:
    from cruProf import app as prof_app
    for rule in prof_app.url_map.iter_rules():
        if rule.endpoint != 'static':
            app.add_url_rule(rule.rule, rule.endpoint, prof_app.view_functions[rule.endpoint], methods=rule.methods)
except ImportError:
    print("Módulo cruProf não encontrado")

try:
    from crudUsuario import app as usuario_app
    for rule in usuario_app.url_map.iter_rules():
        if rule.endpoint != 'static':
            app.add_url_rule(rule.rule, rule.endpoint, usuario_app.view_functions[rule.endpoint], methods=rule.methods)
except ImportError:
    print("Módulo crudUsuario não encontrado")

try:
    from crudTurma import app as turma_app
    for rule in turma_app.url_map.iter_rules():
        if rule.endpoint != 'static':
            app.add_url_rule(rule.rule, rule.endpoint, turma_app.view_functions[rule.endpoint], methods=rule.methods)
except ImportError:
    print("Módulo crudTurma não encontrado")

try:
    from crudPagamento import app as pagamento_app
    for rule in pagamento_app.url_map.iter_rules():
        if rule.endpoint != 'static':
            app.add_url_rule(rule.rule, rule.endpoint, pagamento_app.view_functions[rule.endpoint], methods=rule.methods)
except ImportError:
    print("Módulo crudPagamento não encontrado")

try:
    from crudPresenca import app as presenca_app
    for rule in presenca_app.url_map.iter_rules():
        if rule.endpoint != 'static':
            app.add_url_rule(rule.rule, rule.endpoint, presenca_app.view_functions[rule.endpoint], methods=rule.methods)
except ImportError:
    print("Módulo crudPresenca não encontrado")

try:
    from crudAtividade import app as atividade_app
    for rule in atividade_app.url_map.iter_rules():
        if rule.endpoint != 'static':
            app.add_url_rule(rule.rule, rule.endpoint, atividade_app.view_functions[rule.endpoint], methods=rule.methods)
except ImportError:
    print("Módulo crudAtividade não encontrado")

@app.route('/')
def home():
    return {"message": "API Sistema Escolar", "status": "running"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)