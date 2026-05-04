# ---- Stage 1: builder ----
# Usamos a imagem oficial do Python 3.11 em versão "slim"
# slim = versão reduzida do Linux, sem ferramentas desnecessárias
# O "AS builder" nomeia esse estágio para referenciarmos depois
FROM python:3.11-slim AS builder

# Define o diretório de trabalho DENTRO do container
# É como fazer "cd /app" — todos os comandos seguintes rodam aqui
WORKDIR /app

# Define variáveis de ambiente para otimizar a instalação
# PIP_NO_CACHE_DIR=1 → pip não salva cache (economiza espaço na imagem)
# PYTHONDONTWRITEBYTECODE=1 → Python não gera arquivos .pyc desnecessários
ENV PIP_NO_CACHE_DIR=1 PYTHONDONTWRITEBYTECODE=1

# Atualiza o pip antes de instalar qualquer coisa
RUN pip install --upgrade pip

# Copia SÓ o requirements.txt primeiro (não o projeto inteiro)
# Motivo: Docker tem cache por camada. Se o requirements não mudou,
# ele reaproveita o cache e não reinstala tudo a cada build
COPY requirements.txt .

# Instala as dependências no diretório do usuário (/root/.local)
# --user = instala em /root/.local em vez de no sistema
# Isso permite copiar só essa pasta para o stage 2
RUN pip install --user -r requirements.txt

# ---- Stage 2: runtime ----
# Nova imagem limpa — sem cache do pip, sem ferramentas de build
# Resultado: imagem final muito menor (~150MB vs ~1GB)
FROM python:3.11-slim

WORKDIR /app

# PYTHONUNBUFFERED=1 → Python exibe logs em tempo real no terminal
# (sem isso, os logs ficam em buffer e você não vê nada enquanto roda)
# PATH=... → adiciona /root/.local/bin ao PATH para encontrar os executáveis
# instalados pelo pip (como o uvicorn)
ENV PYTHONUNBUFFERED=1 PATH=/root/.local/bin:$PATH

# Copia SÓ as libs instaladas do stage 1 — sem a bagunça do build
COPY --from=builder /root/.local /root/.local

# Copia o código do projeto
COPY ./app ./app
COPY ./alembic ./alembic
COPY alembic.ini .

# Documenta que o container usa a porta 8000
# Atenção: isso NÃO abre a porta — só é uma documentação
# Quem realmente expõe a porta é o docker-compose.yml
EXPOSE 8000

# Comando que roda quando o container inicia
# Equivale a rodar: uvicorn app.main:app --host 0.0.0.0 --port 8000
# --host 0.0.0.0 → aceita conexões de fora do container (não só localhost)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]