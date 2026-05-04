from pydantic_settings import BaseSettings

# O config.py com pydantic-settings faz basicamente uma coisa só — 
# lê as variáveis do .env e disponibiliza como um objeto Python tipado.


class Settings(BaseSettings):
    # Cada atributo aqui corresponde a uma variável no .env
    # O pydantic-settings lê automaticamente o .env e preenche esses valores
    # Se uma variável obrigatória não existir no .env, ele lança erro na inicialização
    # — muito melhor que descobrir o problema só quando usar a variável
    
    APP_NAME: str
    LOG_LEVEL: str = "INFO"  # valor padrão caso não esteja no .env
    
    # Banco de dados
    DATABASE_URL: str
    DB_ECHO: bool = False
    
    # Scraper
    SCRAPER_MAX_CONCURRENCY: int = 10
    SCRAPER_INTERVAL_MINUTES: int = 60
    SCRAPER_USER_AGENT: str = "JobsScrapper/1.0"

    class Config:
        # Diz ao pydantic-settings para ler o arquivo .env
        env_file = ".env"

# Instância única que será importada pelo resto do projeto
# É isso que o session.py importa com "from app.config import settings"
settings = Settings()