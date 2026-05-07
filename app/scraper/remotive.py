# A função get_jobs recebe o JSON da API do Remotive e 
# extrai as informações relevantes em um formato consistente para o nosso modelo de dados.

from datetime import datetime

def get_jobs(data: dict) -> list[dict]:
    jobs = []

    for job in data.get("jobs", []):
        jobs.append({
            "source": "remotive",
            "external_id": str(job.get("id")),
            "title": job.get("title"),
            "company": job.get("company_name"),
            "category": job.get("category"),
            "salary": job.get("salary"),
            "description": job.get("description"),
            "url": job.get("url"),
            "published_at": datetime.fromisoformat(job.get("publication_date")) if job.get("publication_date") else None,
        })

    return jobs