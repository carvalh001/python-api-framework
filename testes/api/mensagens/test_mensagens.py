"""
Testes do contexto de mensagens (/api/messages).
GET lista, POST criar (com token). Estrutura AAA.
"""
import pytest

from recursos.api.executor_rest import ExecutorRest
from recursos.api.payloads.auth import obter_payload_login
from recursos.api.payloads.mensagens import obter_payload_criar_mensagem
from recursos.utils.gerenciador_configuracao import GerenciadorDeConfiguracao
from recursos.validacao.validadores import validar_campo_presente, validar_status


def _obter_token(executor_rest: ExecutorRest, configuracao: GerenciadorDeConfiguracao) -> str:
    """Faz login e retorna o access_token."""
    payload = obter_payload_login(
        usuario=configuracao.usuario_login or "maria",
        senha=configuracao.senha_login or "123456",
    )
    resposta = executor_rest.requisicao("POST", "/api/auth/login", corpo=payload)
    return resposta.json()["access_token"]


def test_get_mensagens_com_token_retorna_200(
    executor_rest: ExecutorRest,
    configuracao: GerenciadorDeConfiguracao,
) -> None:
    """GET /api/messages com token retorna 200 (lista pode ser vazia)."""
    # Arrange
    token = _obter_token(executor_rest, configuracao)

    # Act
    resposta = executor_rest.requisicao("GET", "/api/messages", token=token)

    # Assert
    validar_status(resposta, 200)
    dados = resposta.json()
    assert isinstance(dados, list)


def test_post_mensagem_com_token_retorna_201_e_campos(
    executor_rest: ExecutorRest,
    configuracao: GerenciadorDeConfiguracao,
) -> None:
    """POST /api/messages com payload fixo retorna 201 e id, titulo, conteudo."""
    # Arrange
    token = _obter_token(executor_rest, configuracao)
    payload = obter_payload_criar_mensagem(
        titulo="Título teste",
        conteudo="Conteúdo da mensagem de teste.",
    )

    # Act
    resposta = executor_rest.requisicao("POST", "/api/messages", corpo=payload, token=token)

    # Assert
    validar_status(resposta, 201)
    dados = resposta.json()
    validar_campo_presente(dados, "id")
    validar_campo_presente(dados, "titulo")
    validar_campo_presente(dados, "conteudo")
