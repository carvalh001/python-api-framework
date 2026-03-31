"""
Payloads para o contexto de autenticação (/api/auth).
Alinhado ao portal-colaborador-backend: login, registro.
"""
import copy
from typing import Any, Dict


def obter_payload_login(usuario: str = "maria", senha: str = "123456") -> Dict[str, Any]:
    """
    Retorna payload para POST /api/auth/login.
    No Arrange, use uma cópia e altere apenas os campos necessários.
    """
    return copy.deepcopy({"username": usuario, "senha": senha})


def obter_payload_registro(
    nome: str = "Usuário Teste",
    email: str = "teste@example.com",
    username: str = "usuarioteste",
    cpf: str = "12345678900",
    telefone: str = "11999999999",
    senha: str = "123456",
    dados_bancarios: Dict[str, str] | None = None,
) -> Dict[str, Any]:
    """
    Retorna payload para POST /api/auth/register.
    """
    payload: Dict[str, Any] = {
        "nome": nome,
        "email": email,
        "username": username,
        "cpf": cpf,
        "telefone": telefone,
        "senha": senha,
    }
    if dados_bancarios:
        payload["dadosBancarios"] = dados_bancarios
    return copy.deepcopy(payload)
