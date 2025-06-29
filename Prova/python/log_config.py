import logging

# Configuração do logging
logging.basicConfig(
    filename='escola_infantil.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def registrar_evento(operacao, aluno_id=None, aluno_nome=None, sucesso=True, mensagem=""):
    """
    Registra um evento no log.
    
    :param operacao: Tipo da operação (CREATE, READ, UPDATE, DELETE)
    :param aluno_id: ID do aluno envolvido
    :param aluno_nome: Nome do aluno
    :param sucesso: Indica se a operação foi bem-sucedida
    :param mensagem: Detalhes adicionais sobre a operação
    """
    status = "SUCESSO" if sucesso else "FALHA"
    log_msg = f"Operação: {operacao} | Aluno ID: {aluno_id} | Nome: {aluno_nome} | Status: {status} | Detalhes: {mensagem}"
    
    if sucesso:
        logging.info(log_msg)
    else:
        logging.error(log_msg)