"""
Testes do contexto de usuários (/api/users).
GET /me, PUT /me (com token). Estrutura AAA.
"""
import pytest

from recursos.api.executor_rest import ExecutorRest
from recursos.api.payloads.auth import obter_payload_login
from recursos.utils.gerenciador_configuracao import GerenciadorDeConfiguracao
from recursos.validacao.validadores import validar_campo_presente, validar_status


def _obter_token(executor_rest: ExecutorRest, configuracao: GerenciadorDeConfiguracao) -> str:
    """Faz login e retorna o access_token."""
    payload = obter_payload_login(
        usuario=configuracao.usuario_login or "maria",
        senha=configuracao.senha_login or "123456",
    )
    resposta = executor_rest.requisicao("POST", "/api/auth/login", corpo=payload)
    dados = resposta.json()
    return dados["access_token"]


def test_get_me_com_token_retorna_200_e_dados_do_usuario(
    executor_rest: ExecutorRest,
    configuracao: GerenciadorDeConfiguracao,
) -> None:
    """GET /api/users/me com token retorna 200 e dados do usuário logado."""
    # Arrange
    token = _obter_token(executor_rest, configuracao)

    # Act
    resposta = executor_rest.requisicao("GET", "/api/users/me", token=token)

    # Assert
    validar_status(resposta, 200)
    dados = resposta.json()
    validar_campo_presente(dados, "id")
    validar_campo_presente(dados, "username")
    validar_campo_presente(dados, "email")


def test_put_me_com_token_retorna_200(
    executor_rest: ExecutorRest,
    configuracao: GerenciadorDeConfiguracao,
) -> None:
    """PUT /api/users/me com token e payload mínimo retorna 200."""
    # Arrange
    token = _obter_token(executor_rest, configuracao)
    payload = {"telefone": "11988887777"}

    # Act
    resposta = executor_rest.requisicao("PUT", "/api/users/me", corpo=payload, token=token)

    # Assert
    validar_status(resposta, 200)
