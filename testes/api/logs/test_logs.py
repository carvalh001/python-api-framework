"""
Testes do contexto de logs (/api/logs).
Requer perfil GESTOR_RH ou ADMIN. GET com token. Estrutura AAA.
"""
import pytest

from recursos.api.executor_rest import ExecutorRest
from recursos.api.payloads.auth import obter_payload_login
from recursos.utils.gerenciador_configuracao import GerenciadorDeConfiguracao
from recursos.validacao.validadores import validar_status


def _obter_token_gestor(executor_rest: ExecutorRest, configuracao: GerenciadorDeConfiguracao) -> str:
    """Login como joao (Gestor RH) para acessar /api/logs."""
    payload = obter_payload_login(usuario="joao", senha=configuracao.senha_login or "123456")
    resposta = executor_rest.requisicao("POST", "/api/auth/login", corpo=payload)
    if resposta.status_code != 200:
        pytest.skip("Usuário joao (Gestor RH) não disponível no ambiente")
    return resposta.json()["access_token"]


def test_get_logs_com_token_gestor_retorna_200(
    executor_rest: ExecutorRest,
    configuracao: GerenciadorDeConfiguracao,
) -> None:
    """GET /api/logs com token de Gestor RH retorna 200 e lista."""
    # Arrange
    token = _obter_token_gestor(executor_rest, configuracao)

    # Act
    resposta = executor_rest.requisicao("GET", "/api/logs", token=token)

    # Assert
    validar_status(resposta, 200)
    dados = resposta.json()
    assert isinstance(dados, list)
