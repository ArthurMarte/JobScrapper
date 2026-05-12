from datetime import datetime
import selectolax

def parse_listing(html: str) -> list[str]:

    final_link = []

    # Usa selectolax para parsear o HTML da descrição da vaga
    parser = selectolax.parser.HTMLParser(html)
    
    # Pega todos os <li> com a classe específica
    elementos = parser.css("li.new-listing-container")

    for elem in elementos:
        # Extrai o link de cada vaga
        link = elem.css_first("a.listing-link--unlocked")
        href = link.attributes.get("href") if link else None

        link_element = "https://weworkremotely.com" + href if href else None
        final_link.append(link_element)

    return final_link



def parse_job_detail(html: str, url: str) -> dict:
    parser = selectolax.parser.HTMLParser(html)

    # ===== Título =====
    title = parser.css_first("h1.lis-container__header__hero__company-info__title")
    title_text = title.text(strip=True) if title else None

    # ===== Empresa =====
    # A empresa está no link que aponta para /company/
    company = parser.css_first("a[href*='/company/']")
    company_text = company.text(strip=True) if company else None

    # ===== Descrição =====
    description = parser.css_first("div.lis-container__job__content__description")
    description_text = description.text(strip=True) if description else None

    # ===== Sidebar (Salary, Job type, Posted on) =====
    # Inicializa os campos como None (caso não existam na página)
    salary_text = None
    category_text = None
    published_at_text = None

    # Pega todos os <li> da sidebar
    sidebar_items = parser.css("ul.lis-container__job__sidebar__job-about__list li")

    for item in sidebar_items:
        # Pega o texto completo do <li> (ex: "Salary $50,000 - $74,999 USD")
        item_text = item.text(strip=True)

        # Identifica qual campo é pelo prefixo do texto
        if item_text.startswith("Salary"):
            # Remove a palavra "Salary" e fica só com o valor
            salary_text = item_text.replace("Salary", "").strip()
        elif item_text.startswith("Job type"):
            category_text = item_text.replace("Job type", "").strip()
        elif item_text.startswith("Posted on"):
            published_at_text = item_text.replace("Posted on", "").strip()

    # ===== External ID (extraído da URL) =====
    # Ex: https://weworkremotely.com/remote-jobs/infiniti-group-ltd-trader
    # split("/")[-1] = "infiniti-group-ltd-trader"
    external_id = url.split("/")[-1]

    return {
        "source": "weworkremotely",
        "external_id": external_id,
        "title": title_text,
        "company": company_text,
        "category": category_text,
        "salary": salary_text,
        "description": description_text,
        "url": url,
        "published_at": None,  # WWR só tem "10 hours ago", não data exata — deixa None
    }