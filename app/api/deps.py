from app.db.session import get_session

# get_db é apenas um alias para get_session
# existe aqui para separar responsabilidades:
# - session.py cuida de COMO a sessão é criada (engine, pool, etc.)
# - deps.py cuida de COMO a API usa essa sessão
# Se um dia precisar adicionar lógica extra (ex: logging, autenticação)
# antes de entregar a sessão para um endpoint, faz aqui sem tocar no session.py
get_db = get_session