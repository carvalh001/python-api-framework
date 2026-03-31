"""
Payloads para o contexto de mensagens (/api/messages).
Alinhado ao portal-colaborador-backend: criar, atualizar mensagem.
"""
import copy
from typing import Any, Dict


def obter_payload_criar_mensagem(
    titulo: str = "Mensagem de teste",
    conteudo: str = "Conteúdo da mensagem de teste.",
) -> Dict[str, Any]:
    """
    Retorna payload para POST /api/messages.
    """
    return copy.deepcopy({"titulo": titulo, "conteudo": conteudo})


def obter_payload_atualizar_mensagem(status: str = "LIDA") -> Dict[str, str]:
    """Retorna payload para PATCH /api/messages/{message_id}."""
    return copy.deepcopy({"status": status})
