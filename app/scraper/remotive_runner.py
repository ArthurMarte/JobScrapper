from app.scraper.client import AsyncScraperClient
from app.scraper.remotive import get_jobs
from app.repositories.job_repo import JobRepository
import structlog
import asyncio
from app.db.session import AsyncSessionLocal
from app.scraper.base_runner import BaseRunner

logger = structlog.get_logger("scraper_runner")


class RemotiveRunner (BaseRunner):
    def __init__(self, client: AsyncScraperClient):
        self.client = client

    async def run(self):
        logger.info("Starting scraper runner")

        # Semaphore limita quantos upserts rodam simultaneamente
        # Sem ele, dispararíamos centenas de inserções de uma vez
        # sobrecarregando o pool de conexões do banco (configurado com 10+20)
        semaphore = asyncio.Semaphore(10)

        # Função interna que envolve o upsert com o controle do semaphore
        # "async with semaphore" → aguarda uma vaga livre antes de executar
        # Cada upsert abre sua própria sessão do banco, garantindo isolamento e evitando bloqueios
        async def upsert_with_semaphore(job_data):
            async with semaphore:
                async with AsyncSessionLocal() as session:
                    repo = JobRepository(session)
                    await repo.upsert(job_data)

        try:
            # Faz a requisição para a API do Remotive
            response = await self.client.get("/api/remote-jobs")

            # Converte a resposta para dicionário Python
            data_not_parsed = response.json()

            # Transforma o JSON em lista de dicts prontos para o upsert
            jobs_parsed = get_jobs(data_not_parsed)

            # Dispara todos os upserts em paralelo, respeitando o semaphore
            # * desempacota o generator em argumentos separados para o gather
            # gather aguarda TODOS terminarem antes de continuar
            await asyncio.gather(*(upsert_with_semaphore(job) for job in jobs_parsed))

        except Exception as e:
            logger.error("Error in scraper runner", error=str(e))

        finally:
            # Sempre fecha o cliente HTTP, mesmo se der erro
            # Sem isso a conexão ficaria aberta indefinidamente
            await self.client.aclose()
            logger.info("Scraper runner finished")