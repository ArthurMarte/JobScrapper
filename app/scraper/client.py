# Camada de transporte HTTP — configura e executa requisições de forma assíncrona
# O client.py é o meio de transporte — ele sabe como fazer requisições HTTP de forma segura e resiliente, mas não sabe o que fazer com o conteúdo que recebe.

import httpx
from tenacity import retry, wait_exponential, stop_after_attempt
import structlog

logger = structlog.get_logger("client_scrapper")

class AsyncScraperClient:
    def __init__(self, base_url:str, timeout:float = 10.0):
        
        # http2=True para usar HTTP/2, que é mais eficiente
        # User-Agent é uma boa prática para evitar bloqueios por parte dos sites — identifica nosso scraper de forma amigável
        # _client é uma conexão HTTP assíncrona que podemos reutilizar para várias requisições, melhorando performance
        self._client = httpx.AsyncClient(base_url=base_url, timeout=timeout, headers={"User-Agent": "JobsScrapper/1.0"}, http2=True)

    # @retry → tenta novamente se falhar, com espera exponencial (2s, 4s, 8s...) até 10s, parando após 3 tentativas
    @retry(wait=wait_exponential(min=2, max=10), stop=stop_after_attempt(3))
    async def get(self, path:str) -> httpx.Response:
        logger.info("ScraperClient GET", path=path)
        response = await self._client.get(path) # Faz a requisição GET para o caminho especificado
        response.raise_for_status() # Lança um erro se a resposta tiver status de erro (4xx ou 5xx)
        return response
    

    async def aclose(self):
        await self._client.aclose() # Fecha a conexão HTTP quando não for mais necessária