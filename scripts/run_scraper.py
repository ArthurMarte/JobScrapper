from app.scraper.runner import ScraperRunner
from app.scraper.client import AsyncScraperClient
from app.db.session import AsyncSessionLocal
import asyncio


async def main():
    # Instancia o client apontando para a base URL do Remotive
    client = AsyncScraperClient(base_url="https://remotive.com")

    # Abre uma sessão do banco e garante que será fechada ao final
    # mesmo se der erro — equivalente ao get_session do FastAPI
    async with AsyncSessionLocal() as session:
        runner = ScraperRunner(client=client)
        await runner.run()


# Ponto de entrada do script — inicia o event loop e executa o main()
# É aqui que o Docker chega quando roda: python -m scripts.run_scraper
asyncio.run(main())