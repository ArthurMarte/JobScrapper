from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.config import settings

# Cria o "motor" de conexão com o banco
# É ele que gerencia o pool de conexões — ou seja, em vez de abrir
# e fechar uma conexão a cada requisição, ele mantém um conjunto
# de conexões reutilizáveis (mais eficiente)
#
# create_async_engine → versão async do engine (usa asyncpg por baixo)
# settings.DATABASE_URL → a URL que você definiu no .env
# echo=settings.DB_ECHO → se True, printa todo SQL executado no terminal
#                         (útil para debug, deixe False em produção)
# pool_size=10 → mantém até 10 conexões abertas simultaneamente
# max_overflow=20 → permite até 20 conexões extras em picos de demanda
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_size=10,
    max_overflow=20,
)

# Fábrica de sessões — é ela que você usa para interagir com o banco
# Analogia com Django: é equivalente ao próprio ORM quando você faz
# Job.objects.all() — a sessão é o "intermediário" entre seu código e o banco
#
# expire_on_commit=False → após um commit, os objetos não expiram
#                          (importante para async, evita queries extras)
# autoflush=False → não envia SQL automaticamente antes de cada query
#                   (você controla quando enviar)
AsyncSessionLocal = async_sessionmaker(
    engine, expire_on_commit=False, autoflush=False
)

# Função geradora que cria uma sessão e garante que ela será fechada
#
# O "yield" faz dela um context manager:
# - tudo antes do yield → abre a sessão
# - seu código usa a sessão
# - tudo depois do yield → fecha a sessão (mesmo se der erro)
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session