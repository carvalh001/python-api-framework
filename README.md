# Framework de Automação de API (Template)

Template de framework de testes de API com Python, organizado por **contexto/funcionalidade**, em **português brasileiro**, usando **pytest** e a estrutura **AAA** (Arrange, Act, Assert). Configuração centralizada no **.env**; acesso apenas via **GerenciadorDeConfiguracao**.

## Estrutura

- **testes/api/** — Testes organizados por funcionalidade (health, auth, usuarios, mensagens, beneficios, logs), cada uma com sua pasta e `test_*.py`.
- **recursos/api/payloads/** — Payloads por contexto (auth.py, usuarios.py, mensagens.py, etc.). No Arrange, use uma cópia e altere só o necessário.
- **recursos/api/executor_rest.py** — Executor REST único: todas as chamadas HTTP passam por ele.
- **recursos/validacao/validadores.py** — Funções de assert comuns (status HTTP, campos JSON); mensagens em PT-BR.
- **recursos/utils/gerenciador_configuracao.py** — Único leitor do .env; expõe URL da API, token, timeouts, etc.

## Pré-requisitos

- Python 3.10+
- API sob teste acessível (ex.: [portal-colaborador-backend](https://github.com/...) rodando em `http://localhost:8000`).

## Setup

Sempre use um ambiente virtual. Passos para **Windows** e **Linux**:

### Windows (PowerShell ou cmd)

```powershell
# Entrar na pasta do projeto
cd python-api-framework

# Criar ambiente virtual
python -m venv .venv

# Ativar o ambiente virtual (PowerShell)
.\.venv\Scripts\Activate.ps1

# Ou no cmd:
# .\.venv\Scripts\activate.bat

# Instalar dependências
pip install -r requirements.txt

# Copiar e configurar o .env
copy .env.example .env
# Edite o arquivo .env com sua URL_BASE_API e credenciais
```

### Linux (bash / sh)

```bash
# Entrar na pasta do projeto
cd python-api-framework

# Criar ambiente virtual
python3 -m venv .venv

# Ativar o ambiente virtual
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Copiar e configurar o .env
cp .env.example .env
# Edite o arquivo .env com sua URL_BASE_API e credenciais
```

### Configuração do .env

Edite o `.env` e defina pelo menos:

- **URL_BASE_API** — URL base da API (ex.: `http://localhost:8000`)
- **USUARIO_LOGIN** e **SENHA_LOGIN** — Credenciais usadas nos testes que fazem login (ex.: maria / 123456 para o portal-colaborador-backend)

O **.env** é o centralizador de variáveis de configuração. Nenhum outro código lê variáveis de ambiente diretamente; use sempre o **GerenciadorDeConfiguracao** (injetado via fixture `configuracao`).

## Executando os testes

Na raiz do projeto (`python-api-framework/`), **com o ambiente virtual ativado**:

```bash
pytest testes/ -v
```

Com relatório JUnit (para CI):

```bash
mkdir -p reports
pytest testes/ --junitxml=reports/junit.xml
python gerar_relatorio.py
```

## Estrutura AAA nos testes

Cada teste segue:

- **# Arrange** — Preparar payload (a partir dos módulos em `recursos/api/payloads/<contexto>.py`), headers, token se necessário.
- **# Act** — Chamar `executor_rest.requisicao(metodo, path, corpo=..., token=...)` e guardar a resposta.
- **# Assert** — Usar as funções de `recursos/validacao/validadores.py`: `validar_status(resposta, 200)`, `validar_campo_presente(dados, "campo")`, etc.

## Exemplo (auth)

```python
# Arrange
payload = obter_payload_login(usuario="maria", senha="123456")

# Act
resposta = executor_rest.requisicao("POST", "/api/auth/login", corpo=payload)

# Assert
validar_status(resposta, 200)
validar_campo_presente(resposta.json(), "access_token")
```

## Cenários de exemplo

Os cenários utilizam o **portal-colaborador-backend** como referência (rotas `/api/auth`, `/api/users`, `/api/benefits`, `/api/messages`, `/api/logs`). Suba o backend e configure `URL_BASE_API` no `.env` para executar os testes.

## CI/CD

O workflow em `.github/workflows/testar-api.yml` executa os testes com pytest, publica resultados JUnit e gera o relatório HTML. Configure no repositório o `URL_BASE_API` (ou use o input no `workflow_dispatch`) para apontar para a API no ambiente desejado.
