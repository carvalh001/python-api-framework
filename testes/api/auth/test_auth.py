"""
Testes do contexto de autenticação (/api/auth).
Login, login com senha inválida, registro. Estrutura AAA.
"""
import pytest

from recursos.api.executor_rest import ExecutorRest
from recursos.api.payloads.auth import obter_payload_login, obter_payload_registro
from recursos.utils.gerenciador_configuracao import GerenciadorDeConfiguracao
from recursos.validacao.validadores import (
    validar_campo_presente,
    validar_campos_obrigatorios,
    validar_status,
)


def test_login_com_credenciais_validas_retorna_200_e_token(
    executor_rest: ExecutorRest,
    configuracao: GerenciadorDeConfiguracao,
) -> None:
    """Login com payload padrão retorna 200, access_token e user."""
    # Arrange
    payload = obter_payload_login(
        usuario=configuracao.usuario_login or "maria",
        senha=configuracao.senha_login or "123456",
    )

    # Act
    resposta = executor_rest.requisicao("POST", "/api/auth/login", corpo=payload)

    # Assert
    validar_status(resposta, 200)
    dados = resposta.json()
    validar_campos_obrigatorios(dados, ["access_token", "token_type", "user"])
    validar_campo_presente(dados, "access_token")
    assert len(dados["access_token"]) > 0


def test_login_com_senha_invalida_retorna_401(
    executor_rest: ExecutorRest,
    configuracao: GerenciadorDeConfiguracao,
) -> None:
    """Login com senha incorreta retorna 401."""
    # Arrange
    payload = obter_payload_login(
        usuario=configuracao.usuario_login or "maria",
        senha="senha_errada_123",
    )

    # Act
    resposta = executor_rest.requisicao("POST", "/api/auth/login", corpo=payload)

    # Assert
    validar_status(resposta, 401)


def test_registro_de_novo_usuario_retorna_201_e_campos_esperados(
    executor_rest: ExecutorRest,
) -> None:
    """Registro com payload válido retorna 201 e dados do usuário."""
    # Arrange — usar username/email únicos para evitar conflito
    import uuid
    sufixo = uuid.uuid4().hex[:8]
    payload = obter_payload_registro(
        nome="Usuário Teste Registro",
        email=f"teste{sufixo}@example.com",
        username=f"user{sufixo}",
        cpf=f"111{sufixo[:8]}",
        telefone="11999999999",
        senha="123456",
    )

    # Act
    resposta = executor_rest.requisicao("POST", "/api/auth/register", corpo=payload)

    # Assert
    validar_status(resposta, 201)
    dados = resposta.json()
    validar_campo_presente(dados, "id")
    validar_campo_presente(dados, "username")
    validar_campo_presente(dados, "email")
