"""
Parâmetros para o contexto de logs (/api/logs).
GET com filtros: user_id, event_type, start_date, end_date, skip, limit.
"""
import copy
from typing import Any, Dict, Optional


def obter_params_listar_logs(
    user_id: Optional[int] = None,
    event_type: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
) -> Dict[str, Any]:
    """
    Retorna query params para GET /api/logs.
    """
    params: Dict[str, Any] = {"skip": skip, "limit": limit}
    if user_id is not None:
        params["user_id"] = user_id
    if event_type is not None:
        params["event_type"] = event_type
    if start_date is not None:
        params["start_date"] = start_date
    if end_date is not None:
        params["end_date"] = end_date
    return copy.deepcopy(params)
