from app.scraper.remotive_runner import RemotiveRunner
from app.scraper.weworkremotely_runner import WeWorkRemotelyRunner
from app.scraper.client import AsyncScraperClient
from app.db.session import AsyncSessionLocal
import asyncio


async def main():
    # Instancia o client apontando para a base URL do Remotive
    client1 = AsyncScraperClient(base_url="https://remotive.com")
    client2 = AsyncScraperClient(base_url="https://weworkremotely.com")

    # Abre uma sessão do banco e garante que será fechada ao final
    # mesmo se der erro — equivalente ao get_session do FastAPI
    runner = RemotiveRunner(client=client1)
    await runner.run()

    runner2 = WeWorkRemotelyRunner(client=client2)
    await runner2.run()


# Ponto de entrada do script — inicia o event loop e executa o main()
# É aqui que o Docker chega quando roda: python -m scripts.run_scraper
asyncio.run(main())