"""
Fixtures do pytest para o framework de automação de API.
Configuração e executor REST são fornecidos aqui; use nos testes com # Arrange / # Act / # Assert.
"""
import pytest

from recursos.api.executor_rest import ExecutorRest
from recursos.utils.gerenciador_configuracao import GerenciadorDeConfiguracao


@pytest.fixture(scope="session")
def configuracao() -> GerenciadorDeConfiguracao:
    """Gerenciador de configuração (lê .env). Único ponto de acesso às variáveis de ambiente."""
    return GerenciadorDeConfiguracao()


@pytest.fixture(scope="session")
def executor_rest(configuracao: GerenciadorDeConfiguracao) -> ExecutorRest:
    """Executor REST único. Use para todas as chamadas HTTP nos testes."""
    return ExecutorRest(configuracao)
