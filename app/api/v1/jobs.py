from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.schemas.job import JobOut, JobList
from app.repositories.job_repo import JobRepository

router = APIRouter(prefix="/jobs", tags=["jobs"])

# Endpoint para buscar uma vaga específica pelo ID
# GET /api/v1/jobs/{job_id}
# response_model=JobOut → FastAPI usa o schema JobOut para formatar a resposta filtra campos, converte tipos, tudo automaticamente
@router.get("/{job_id}", response_model=JobOut)
async def get_job(job_id: int, db: AsyncSession = Depends(get_db)):
    # Instancia o repositório passando a sessão do banco
    # O repositório centraliza todo acesso ao banco — não fazemos queries direto aqui
    repo = JobRepository(db)

    # Chama o método get_by_id que criamos no repositório
    # Retorna o objeto Job ou None se não existir
    job = await repo.get_by_id(job_id)

    # Se não encontrou, lança erro 404
    # HTTPException é o jeito correto no FastAPI — não retorne dicionários de erro
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    # Retorna o objeto Job — o FastAPI converte para JobOut automaticamente
    # graças ao response_model e ao model_config = ConfigDict(from_attributes=True)
    return job



# Endpoint para listar vagas com paginação
# Parâmetros opcionais de filtro — vêm direto da query string
# Ex: /api/v1/jobs?title=python&category=backend&page=2
#
# page  → qual página o cliente está pedindo (ex: página 2)
# size  → quantos itens por página (ex: 20)
# total → permite o frontend calcular quantas páginas existem no total
# ex: total=150 com size=20 = 8 páginas
@router.get("", response_model=JobList)
async def list_jobs(title: str | None = None, category: str | None = None, company: str | None = None, page: int = 1, size: int = 20, db: AsyncSession = Depends(get_db)): 
    repo = JobRepository(db)

    # Chama o método de listagem do repositório, passando os filtros e paginação
    jobs, total = await repo.search(title=title, category=category, company=company, page=page, size=size)

    # Retorna a lista de vagas e o total para a resposta
    return JobList(items=jobs, total=total, page=page, size=size)



#Parâmetro no path (/{job_id}) → sempre obrigatório — faz parte da URL
#Parâmetro na função sem valor padrão (title: str) → obrigatório
#Parâmetro na função com = None (title: str | None = None) → opcional
#Parâmetro na função com valor padrão (page: int = 1) → opcional com default