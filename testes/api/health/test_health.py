"""
Testes do endpoint de health check (/health).
Sem autenticação. Estrutura AAA (Arrange, Act, Assert).
"""
import pytest

from recursos.api.executor_rest import ExecutorRest
from recursos.validacao.validadores import validar_status


def test_health_retorna_200(executor_rest: ExecutorRest) -> None:
    """GET /health retorna status 200."""
    # Arrange
    # (nenhum payload; endpoint público)

    # Act
    resposta = executor_rest.requisicao("GET", "/health")

    # Assert
    validar_status(resposta, 200)
