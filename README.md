# Mars Probe API

API REST para controlar sondas exploratórias em Marte. As sondas navegam em um planalto retangular por meio de comandos de movimento e rotação.

## Requisitos

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recomendado) ou pip

## Instalação

```bash
# com uv (recomendado)
uv sync

# ou com pip
pip install -e ".[dev]"
```

## Executando

```bash
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`.  
Documentação interativa: `http://localhost:8000/docs`

## Testes

```bash
pytest
```

## Docker

```bash
docker compose up --build
```

A API ficará disponível em `http://localhost:8000`.

## Endpoints

### POST /probes
Lança uma sonda e define o tamanho da malha.

```json
{
    "x": 5,
    "y": 5,
    "direction": "NORTH"
}
```

A sonda sempre inicia em `(0, 0)`. Os valores `x` e `y` representam o canto superior direito da malha disponível.

**Resposta (201):**
```json
{
    "id": "abc123",
    "x": 0,
    "y": 0,
    "direction": "NORTH"
}
```

---

### PATCH /probes/{id}/commands
Envia uma sequência de comandos para mover a sonda.

```json
{
    "commands": "MRM"
}
```

Comandos disponíveis:
- `M` — move 1 espaço na direção atual
- `L` — rotaciona 90° para a esquerda (sem se mover)
- `R` — rotaciona 90° para a direita (sem se mover)

Os comandos são case-insensitive. Se qualquer comando for inválido, ou se o movimento ultrapassar os limites da malha, **nenhum comando é executado** e um erro é retornado.

**Resposta (200):**
```json
{
    "id": "abc123",
    "x": 1,
    "y": 1,
    "direction": "EAST"
}
```

**Erros:**
- `404` — sonda não encontrada
- `422` — comando inválido ou movimento fora dos limites da malha

---

### GET /probes
Retorna o estado atual de todas as sondas.

**Resposta (200):**
```json
{
    "probes": [
        {
            "id": "abc123",
            "x": 1,
            "y": 1,
            "direction": "EAST"
        },
        {
            "id": "xyzbas1234",
            "x": 3,
            "y": 4,
            "direction": "NORTH"
        }
    ]
}
```

## Estrutura do projeto

```
app/
  main.py                ponto de entrada da aplicação
  models/
    probe.py             schemas Pydantic e enums (Direction, Probe, requests)
  routers/
    probes.py            endpoints HTTP
  services/
    probe_service.py     lógica de negócio e exceções de domínio
  storage/
    database.py          configuração SQLAlchemy e get_session
    models.py            modelo ORM (ProbeRecord)
    repository.py        acesso ao banco de dados
    memory.py            implementação alternativa em memória
tests/
  conftest.py            fixture com SQLite in-memory para testes isolados
  test_launch.py         testes do endpoint de lançamento
  test_movement.py       testes de movimento e validações
  test_status.py         testes do endpoint de listagem
```

## Tecnologias

- **FastAPI** — framework web
- **SQLAlchemy** — ORM com SQLite para persistência
- **Pydantic** — validação de dados e schemas
- **uv** — gerenciamento de dependências
- **pytest** — testes automatizados
- **Docker** — containerização
