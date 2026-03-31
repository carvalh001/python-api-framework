"""
Testes do contexto de benefícios (/api/benefits).
GET com token retorna lista. Estrutura AAA.
"""
import pytest

from recursos.api.executor_rest import ExecutorRest
from recursos.api.payloads.auth import obter_payload_login
from recursos.utils.gerenciador_configuracao import GerenciadorDeConfiguracao
from recursos.validacao.validadores import validar_status


def _obter_token(executor_rest: ExecutorRest, configuracao: GerenciadorDeConfiguracao) -> str:
    """Faz login e retorna o access_token."""
    payload = obter_payload_login(
        usuario=configuracao.usuario_login or "maria",
        senha=configuracao.senha_login or "123456",
    )
    resposta = executor_rest.requisicao("POST", "/api/auth/login", corpo=payload)
    return resposta.json()["access_token"]


def test_get_beneficios_com_token_retorna_200_e_lista(
    executor_rest: ExecutorRest,
    configuracao: GerenciadorDeConfiguracao,
) -> None:
    """GET /api/benefits com token retorna 200 e array (lista de benefícios)."""
    # Arrange
    token = _obter_token(executor_rest, configuracao)

    # Act
    resposta = executor_rest.requisicao("GET", "/api/benefits", token=token)

    # Assert
    validar_status(resposta, 200)
    dados = resposta.json()
    assert isinstance(dados, list)
