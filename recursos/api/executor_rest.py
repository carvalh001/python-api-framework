"""
Executor REST único (factory).

Centraliza todas as chamadas HTTP. Recebe a configuração do GerenciadorDeConfiguracao
e expõe um único método para realizar requisições (GET, POST, PUT, PATCH, DELETE).
"""
import copy
from typing import Any

import requests

from recursos.utils.gerenciador_configuracao import GerenciadorDeConfiguracao


class RespostaRest:
    """Objeto que encapsula a resposta HTTP para uso nos asserts."""

    def __init__(self, response: requests.Response) -> None:
        self._response = response

    @property
    def status_code(self) -> int:
        """Código de status HTTP."""
        return self._response.status_code

    @property
    def headers(self) -> dict:
        """Cabeçalhos da resposta."""
        return dict(self._response.headers)

    def json(self) -> Any:
        """Corpo da resposta como JSON (dict/list)."""
        try:
            return self._response.json()
        except ValueError:
            return None

    @property
    def text(self) -> str:
        """Corpo da resposta como texto."""
        return self._response.text


class ExecutorRest:
    """
    Executor REST único. Realiza requisições usando a URL base e configurações
    do GerenciadorDeConfiguracao. Injeta token Bearer quando configurado.
    """

    def __init__(self, configuracao: GerenciadorDeConfiguracao) -> None:
        self._config = configuracao

    def requisicao(
        self,
        metodo: str,
        path: str,
        corpo: dict | None = None,
        headers: dict | None = None,
        params: dict | None = None,
        token: str | None = None,
    ) -> RespostaRest:
        """
        Executa uma requisição HTTP.

        Args:
            metodo: GET, POST, PUT, PATCH, DELETE.
            path: Caminho do endpoint (ex.: /api/auth/login). Será concatenado à URL base.
            corpo: Corpo da requisição (JSON). None para GET etc.
            headers: Cabeçalhos adicionais. Authorization pode ser sobrescrito.
            params: Query string (dict).
            token: Token Bearer para esta requisição. Se None, usa config.api_token se existir.

        Returns:
            RespostaRest com status_code, headers, .json(), .text.
        """
        url = f"{self._config.url_base_api}{path}" if path.startswith("/") else f"{self._config.url_base_api}/{path}"
        cabecalhos = copy.deepcopy(headers) if headers else {}
        if "Content-Type" not in cabecalhos and corpo is not None:
            cabecalhos["Content-Type"] = "application/json"
        token_a_usar = token if token is not None else self._config.api_token
        if token_a_usar:
            cabecalhos["Authorization"] = f"Bearer {token_a_usar}"

        response = requests.request(
            method=metodo.upper(),
            url=url,
            json=corpo,
            headers=cabecalhos or None,
            params=params,
            timeout=self._config.api_timeout,
            verify=self._config.verificar_ssl,
        )
        return RespostaRest(response)
