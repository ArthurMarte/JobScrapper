from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Job  # O modelo do banco de dados
from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert # Para upsert (insert ou update)


class JobRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    
    async def get_by_id(self, id: int) -> Job | None:
        # "await" pausa a execução e espera o banco responder
        # sem ele, a query não seria executada de verdade
        # 
        # self.db.get(Job, id) é equivalente a:
        # SELECT * FROM jobs WHERE id = {id} LIMIT 1
        #
        # Retorna o objeto Job se encontrar, ou None se não existir
        return await self.db.get(Job, id)
    


    async def search(self, title: str | None = None, category: str | None = None, company: str | None = None, page: int = 1, size: int = 20) -> tuple[list[Job], int]:
        # Busca vagas por título, categoria e empresa, com paginação

        # Começa a query base — equivalente ao Job.objects.all() do Django
        query = select(Job)

        if title:
            title = f"%{title.lower()}%"
            # Acessa a tabela Job e filtra por titulo 
            query = query.where(Job.title.ilike(title)) # ilike → busca case-insensitive, % é wildcard (qualquer coisa antes/depois)

        if category:
            category = f"%{category.lower()}%"
            query = query.where(Job.category.ilike(category))

        if company:
            company = f"%{company.lower()}%"
            query = query.where(Job.company.ilike(company))

        # Conta o total ANTES de paginar
        # Isso permite retornar "total: 150" mesmo mostrando só 20 por página
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.db.scalar(count_query)

        # Aplica paginação
        # offset = quantos registros pular (página 2 com size 20 = pula 20)
        # limit = quantos registros retornar
        query = query.offset((page - 1) * size).limit(size)

        # Executa a query e retorna os resultados
        result = await self.db.execute(query)
        jobs = result.scalars().all()

        return jobs, total

        

    async def upsert(self, job_data: dict) -> None:
        # Recebe os dados da vaga como dicionário
        # Ex: {"source": "remotive", "external_id": "123", "title": "Backend Dev", ...}

        # insert(Job) → cria um statement de INSERT na tabela jobs
        # .values(**job_data) → desempacota o dicionário como colunas/valores equivalente a passar title="Backend Dev", company="Acme", etc.
        # .on_conflict_do_nothing() → se já existir uma vaga com a mesma source + external_id (UniqueConstraint do model), ignora silenciosamente
        #  equivalente ao SQL: INSERT ... ON CONFLICT DO NOTHING
        # index_elements → diz quais colunas formam o conflito (as do UniqueConstraint)
        stmt = insert(Job).values(**job_data).on_conflict_do_nothing(
            index_elements=["source", "external_id"]
        )

        # Executa o statement no banco
        await self.db.execute(stmt)

        # Confirma a transação — sem isso o insert ficaria pendente
        # e seria descartado quando a sessão fechasse
        # Operações de leitura (search, get_by_id) não precisam de commit
        # porque não alteram dados
        await self.db.commit()
