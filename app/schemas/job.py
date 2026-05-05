from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# Schema para retornar os dados de um job
class JobOut(BaseModel):
    id: int
    source: str
    title: str
    description: Optional[str] = None
    company: Optional[str] = None
    category: Optional[str] = None
    salary: Optional[str] = None
    url: str
    published_at: Optional[datetime] = None

    # Permite que o Pydantic leia objetos do SQLAlchemy diretamente
    # Sem isso, só funcionaria com dicionários
    model_config = ConfigDict(from_attributes=True)


# Schema para retornar uma lista paginada de vagas
# total → quantidade total de vagas no banco
# page e size → para o frontend saber em qual página está
class JobList(BaseModel):
    items: list[JobOut]
    total: int
    page: int
    size: int