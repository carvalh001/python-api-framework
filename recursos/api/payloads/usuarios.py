"""
Payloads para o contexto de usuários (/api/users).
Alinhado ao portal-colaborador-backend: atualizar me, role.
"""
import copy
from typing import Any, Dict, Optional


def obter_payload_atualizar_me(
    nome: Optional[str] = None,
    email: Optional[str] = None,
    telefone: Optional[str] = None,
    dados_bancarios: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    Retorna payload para PUT /api/users/me.
    Inclua apenas os campos que deseja alterar.
    """
    payload: Dict[str, Any] = {}
    if nome is not None:
        payload["nome"] = nome
    if email is not None:
        payload["email"] = email
    if telefone is not None:
        payload["telefone"] = telefone
    if dados_bancarios is not None:
        payload["dadosBancarios"] = dados_bancarios
    return copy.deepcopy(payload)


def obter_payload_atualizar_role(papel: str = "COLABORADOR") -> Dict[str, str]:
    """Retorna payload para PATCH /api/users/{user_id}/role."""
    return copy.deepcopy({"papel": papel})
