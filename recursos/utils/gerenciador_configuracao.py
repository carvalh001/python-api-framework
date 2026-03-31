"""
Gerenciador de configuração do framework de automação de API.
É o ÚNICO módulo que lê o arquivo .env. Toda variável de configuração
deve estar no .env e ser acessada apenas através desta classe.
O .env é o centralizador; este gerenciador é a única porta de entrada.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class GerenciadorDeConfiguracao:
    """
    Gerencia as variáveis de ambiente que estão no .env.
    Carrega o arquivo .env e expõe os valores para o resto do framework.
    """

    def __init__(self, arquivo_env: str = ".env") -> None:
        """
        Inicializa o gerenciador e carrega as configurações do arquivo .env.

        Args:
            arquivo_env: Caminho para o arquivo .env (padrão: ".env" na raiz do projeto)
        """
        self._caminho_raiz_projeto = Path(__file__).resolve().parent.parent.parent
        self._caminho_arquivo_env = self._caminho_raiz_projeto / arquivo_env
        self._carregar_variaveis_ambiente()
        self._validar_configuracoes_obrigatorias()

    def _carregar_variaveis_ambiente(self) -> None:
        """Carrega as variáveis de ambiente do arquivo .env."""
        if self._caminho_arquivo_env.exists():
            load_dotenv(self._caminho_arquivo_env)
        else:
            raise FileNotFoundError(
                f"Arquivo .env não encontrado em: {self._caminho_arquivo_env}. "
                "Copie o .env.example para .env e configure."
            )

    def _validar_configuracoes_obrigatorias(self) -> None:
        """Valida se as configurações obrigatórias estão presentes."""
        if not self._obter_valor("URL_BASE_API"):
            raise ValueError(
                "Configuração obrigatória 'URL_BASE_API' não encontrada no arquivo .env"
            )

    def _obter_valor(self, chave: str, valor_padrao: Optional[str] = None) -> Optional[str]:
        """Obtém um valor de configuração do ambiente."""
        return os.getenv(chave, valor_padrao)

    def _obter_booleano(self, chave: str, valor_padrao: bool = False) -> bool:
        """Obtém um valor booleano de configuração."""
        valor = self._obter_valor(chave, str(valor_padrao))
        return str(valor).lower() in ("true", "yes", "1", "sim", "verdadeiro")

    def _obter_inteiro(self, chave: str, valor_padrao: int = 0) -> int:
        """Obtém um valor inteiro de configuração."""
        valor = self._obter_valor(chave, str(valor_padrao))
        try:
            return int(valor)
        except (ValueError, TypeError):
            return valor_padrao

    @property
    def url_base_api(self) -> str:
        """URL base da API sob teste."""
        return self._obter_valor("URL_BASE_API", "http://localhost:8000").rstrip("/")

    @property
    def api_token(self) -> str:
        """Token de autenticação para API (Bearer)."""
        return self._obter_valor("API_TOKEN", "")

    @property
    def usuario_login(self) -> str:
        """Usuário para login nos testes."""
        return self._obter_valor("USUARIO_LOGIN", "")

    @property
    def senha_login(self) -> str:
        """Senha para login nos testes."""
        return self._obter_valor("SENHA_LOGIN", "")

    @property
    def api_timeout(self) -> int:
        """Timeout em segundos para requisições HTTP."""
        return self._obter_inteiro("API_TIMEOUT", 30)

    @property
    def verificar_ssl(self) -> bool:
        """Se deve verificar certificados SSL nas requisições."""
        return self._obter_booleano("API_VERIFICAR_SSL", False)

    @property
    def diretorio_relatorios(self) -> Path:
        """Diretório raiz para relatórios."""
        return Path(self._obter_valor("DIRETORIO_RELATORIOS", "./reports"))

    @property
    def nivel_log(self) -> str:
        """Nível de log (DEBUG, INFO, WARNING, ERROR)."""
        return (self._obter_valor("NIVEL_LOG", "INFO") or "INFO").upper()
