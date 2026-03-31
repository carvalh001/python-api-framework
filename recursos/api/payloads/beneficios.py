"""
Payloads e parâmetros para o contexto de benefícios (/api/benefits).
O backend expõe principalmente GET com query params (user_id, categoria, status).
"""
import copy
from typing import Any, Dict, Optional


def obter_params_listar_beneficios(
    user_id: Optional[int] = None,
    categoria: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
) -> Dict[str, Any]:
    """
    Retorna query params para GET /api/benefits.
    """
    params: Dict[str, Any] = {"skip": skip, "limit": limit}
    if user_id is not None:
        params["user_id"] = user_id
    if categoria is not None:
        params["categoria"] = categoria
    if status is not None:
        params["status"] = status
    return copy.deepcopy(params)
