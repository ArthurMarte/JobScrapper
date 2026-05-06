from fastapi import FastAPI
from app.api.v1 import jobs  # Importa as rotas dos endpoints de jobs


# Cria a instância principal da aplicação
# É esse objeto "app" que o Uvicorn procura quando você escreve
# "uvicorn app.main:app" no docker-compose

app = FastAPI(
    # Nome que aparece na documentação automática (/docs)
    title="JobsScrapper API",
    # Descrição que aparece no /docs
    description="API para consulta de vagas coletadas pelo scraper",
    # Versão da API — boa prática manter atualizado
    version="0.1.0",
)

# Rota de health check — usada para verificar se a API está de pé
# É uma convenção de mercado ter um /health em toda API
@app.get("/health")
async def health():
    return {"status": "ok", "service": "JobsScrapper API"}

# Importa as rotas dos endpoints — isso é necessário para que o FastAPI registre as rotas
app.include_router(jobs.router, prefix="/api/v1")  # Todas as rotas do jobs vão começar com /api/v1