from sqlalchemy import String, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.base import Base



# Cada coluna tem tipo Python (Mapped[str]) para o código e tipo banco (String(50)) 
# para o SQL — quando um não precisa de configuração extra, você pode omitir o tipo banco.

class Job(Base):
    __tablename__ = "jobs"

    # UniqueConstraint garante que não vai ter vaga duplicada no banco
    # A combinação source + external_id é única — ou seja, a mesma vaga
    # do mesmo site não pode ser inserida duas vezes
    # Table args é uma forma de passar opções adicionais para a tabela, como constraints
    __table_args__ = (UniqueConstraint("source", "external_id"),)

    # Mapped[int] → tipo da coluna (inteiro)
    # primary_key=True → chave primária, gerada automaticamente
    id: Mapped[int] = mapped_column(primary_key=True)

    # De qual site veio a vaga ("remotive", "remoteok", etc.)
    # index=True → cria índice no banco, acelera buscas por esse campo
    source: Mapped[str] = mapped_column(String(50), index=True)

    # ID da vaga no site de origem
    # Combinado com source forma a chave única definida acima
    external_id: Mapped[str] = mapped_column(String(120))

    # index=True porque você vai buscar vagas por título frequentemente
    title: Mapped[str] = mapped_column(String(255), index=True)

    company: Mapped[str] = mapped_column(String(120))

    # str | None → campo opcional (pode ser nulo)
    # nullable=True → permite NULL no banco
    category: Mapped[str | None] = mapped_column(String(80), nullable=True)
    salary: Mapped[str | None] = mapped_column(String(120), nullable=True)
    description: Mapped[str | None] = mapped_column(nullable=True)

    url: Mapped[str] = mapped_column(String(500))

    # Data de publicação no site de origem (pode não existir em todos os sites)
    published_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Data em que o scraper coletou essa vaga — sempre preenchida
    scraped_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)