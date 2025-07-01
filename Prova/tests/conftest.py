import pytest
from flask import Flask
import sys
import os

# Adiciona o diretório raiz do projeto ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def app():
    """Cria uma instância Flask para testes."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['DATABASE_URL'] = 'sqlite:///:memory:'  # Banco em memória para testes
    
    # Importa e registra as rotas dos módulos
    try:
        from App.crudAlunos import app as alunos_app
        for rule in alunos_app.url_map.iter_rules():
            if rule.endpoint != 'static':
                app.add_url_rule(rule.rule, rule.endpoint, alunos_app.view_functions[rule.endpoint], methods=rule.methods)
    except ImportError:
        pass
    
    try:
        from App.crudUsuario import app as usuarios_app
        for rule in usuarios_app.url_map.iter_rules():
            if rule.endpoint != 'static':
                app.add_url_rule(rule.rule, rule.endpoint, usuarios_app.view_functions[rule.endpoint], methods=rule.methods)
    except ImportError:
        pass
    
    try:
        from App.cruProf import app as prof_app
        for rule in prof_app.url_map.iter_rules():
            if rule.endpoint != 'static':
                app.add_url_rule(rule.rule, rule.endpoint, prof_app.view_functions[rule.endpoint], methods=rule.methods)
    except ImportError:
        pass
    
    return app

@pytest.fixture
def client(app):
    """Um cliente de teste para o app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Um runner de teste para os comandos CLI do app."""
    return app.test_cli_runner()