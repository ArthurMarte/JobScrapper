from abc import ABC, abstractmethod


# ABC (Abstract Base Class) → classe especial do Python que permite definir métodos abstratos
# @abstractmethod → marca um método como obrigatório; classes filhas precisam implementá-lo
class BaseRunner(ABC):
    """
    Classe base abstrata para todos os runners de scraping.
    Cada fonte (Remotive, WeWorkRemotely, etc.) implementa sua própria
    lógica de coleta dentro do método run().
    """

    @abstractmethod
    async def run(self):
        """Executa o scraping da fonte específica."""
        pass