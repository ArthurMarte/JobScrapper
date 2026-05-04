from sqlalchemy.orm import DeclarativeBase

# Base é a "classe mãe" de todos os seus models
# Todo model (Job, Company, Tag...) vai herdar dela
# É ela que diz ao SQLAlchemy: "esses são os objetos que
# representam tabelas no banco"
#
# Analogia com Django: é equivalente ao models.Model
# Quando você fazia "class Job(models.Model)" no Django,
# estava fazendo a mesma coisa — herdando de uma base
# que o Django usa para mapear sua classe para uma tabela
#
# O SQLAlchemy precisa de uma Base centralizada para:
# 1. Saber quais classes são tabelas
# 2. Gerar as migrations pelo Alembic
# 3. Criar/dropar tabelas nos testes
class Base(DeclarativeBase):
    pass