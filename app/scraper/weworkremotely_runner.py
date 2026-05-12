from app.scraper.base_runner import BaseRunner
from app.scraper.client import AsyncScraperClient
from app.scraper.weworkremotely import parse_listing, parse_job_detail
from app.repositories.job_repo import JobRepository
from app.db.session import AsyncSessionLocal
import structlog
import asyncio

logger = structlog.get_logger("weworkremotely_runner")


class WeWorkRemotelyRunner(BaseRunner):
    def __init__(self, client: AsyncScraperClient):
        self.client = client

    async def run(self):
        logger.info("Starting WeWorkRemotely runner")

        # Semaphore limita requisições HTTP simultâneas
        # ao site (não ao banco, como no Remotive)
        semaphore = asyncio.Semaphore(10)

        # Função interna: faz scraping de uma vaga e salva no banco
        # Encapsula tudo: requisição HTTP + parse + upsert
        async def scrape_and_save(url: str):
            async with semaphore:
                try:
                    # ... aqui você implementa:
                    # 1. Fazer requisição HTTP para a URL da vaga
                    response = await self.client.get(url)
                    # 2. Parsear o HTML
                    job_data = parse_job_detail(response.text, url)
                    # 3. Abrir sessão do banco e fazer upsert
                    async with AsyncSessionLocal() as session:
                        repo = JobRepository(session)
                        await repo.upsert(job_data)
                except Exception as e:
                    logger.error("Error scraping job", url=url, error=str(e))

        try:
            # 1. Pega o HTML da listagem
            response = await self.client.get("")

            # 2. Extrai todas as URLs das vagas
            job_urls = parse_listing(response.text)

            # 3. Dispara scraping de todas as vagas em paralelo (com semaphore)
            await asyncio.gather(*(scrape_and_save(url) for url in job_urls))

        except Exception as e:
            logger.error("Error in WeWorkRemotely runner", error=str(e))

        finally:
            await self.client.aclose()
            logger.info("WeWorkRemotely runner finished")