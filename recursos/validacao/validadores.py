"""
Biblioteca de validação comum para o bloco # Assert.
Mensagens de falha em português. Use apenas estas funções nos testes.
"""
from typing import Any, List, Optional

from recursos.api.executor_rest import RespostaRest


def validar_status(resposta: RespostaRest, status_esperado: int) -> None:
    """
    Verifica se o status HTTP da resposta é o esperado.
    Levanta AssertionError com mensagem em PT-BR em caso de falha.
    """
    if resposta.status_code != status_esperado:
        raise AssertionError(
            f"Status HTTP incorreto. Esperado: {status_esperado}, "
            f"Obtido: {resposta.status_code}. Corpo: {resposta.text[:500]}"
        )


def validar_campo_presente(dados: Optional[dict], nome_campo: str) -> None:
    """
    Verifica se o campo existe no dicionário (pode ser None como valor).
    Levanta AssertionError com mensagem em PT-BR se o campo não existir.
    """
    if dados is None:
        raise AssertionError(
            f"Resposta não é um JSON válido (ou é nula). "
            f"Não foi possível verificar o campo '{nome_campo}'."
        )
    if nome_campo not in dados:
        raise AssertionError(
            f"Campo obrigatório '{nome_campo}' não encontrado na resposta. "
            f"Campos presentes: {list(dados.keys())}"
        )


def validar_campo_valor(
    dados: Optional[dict],
    nome_campo: str,
    valor_esperado: Any,
) -> None:
    """
    Verifica se o campo existe e tem o valor esperado.
    Levanta AssertionError com mensagem em PT-BR em caso de falha.
    """
    validar_campo_presente(dados, nome_campo)
    valor_obtido = dados.get(nome_campo)
    if valor_obtido != valor_esperado:
        raise AssertionError(
            f"Valor do campo '{nome_campo}' incorreto. "
            f"Esperado: {valor_esperado!r}, Obtido: {valor_obtido!r}"
        )


def validar_campos_obrigatorios(dados: Optional[dict], lista_campos: List[str]) -> None:
    """
    Verifica se todos os campos da lista existem no dicionário.
    Levanta AssertionError com mensagem em PT-BR listando os que faltam.
    """
    if dados is None:
        raise AssertionError(
            "Resposta não é um JSON válido (ou é nula). "
            f"Não foi possível verificar os campos: {lista_campos}"
        )
    faltando = [c for c in lista_campos if c not in dados]
    if faltando:
        raise AssertionError(
            f"Campos obrigatórios não encontrados na resposta: {faltando}. "
            f"Campos presentes: {list(dados.keys())}"
        )
