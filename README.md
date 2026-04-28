# Mars Probe API

API REST para controlar sondas exploratórias em Marte. As sondas navegam em um planalto retangular por meio de comandos de movimento e rotação.

## Requisitos

- Python 3.11+
- pip

## Instalação

```bash
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

## Endpoints

### POST /probes
Lança uma sonda nova e define o tamanho da malha.

```json
{
    "x": 5,
    "y": 5,
    "direction": "NORTH"
}
```

A sonda sempre inicia em `(0, 0)`. Os valores `x` e `y` representam o canto superior direito da malha.

**Resposta:**
```json
{
    "id": "abc123",
    "x": 0,
    "y": 0,
    "direction": "NORTH"
}
```

### PATCH /probes/{id}/commands
Envia uma sequência de comandos para a sonda.

```json
{
    "commands": "MRM"
}
```

Comandos disponíveis:
- `M` — move 1 espaço na direção atual
- `L` — rotaciona 90° para a esquerda
- `R` — rotaciona 90° para a direita

Comandos são case-insensitive. Se qualquer comando for inválido, ou se algum movimento ultrapassar os limites da malha, a sonda não executa nenhum comando e um erro é retornado.

**Resposta:**
```json
{
    "id": "abc123",
    "x": 1,
    "y": 1,
    "direction": "EAST"
}
```

### GET /probes
Retorna o estado atual de todas as sondas.

**Resposta:**
```json
{
    "probes": [
        {
            "id": "abc123",
            "x": 1,
            "y": 1,
            "direction": "EAST"
        }
    ]
}
```

## Estrutura do projeto

```
app/
  main.py            ponto de entrada da aplicação
  routers/
    probes.py        endpoints HTTP
  models/
    probe.py         schemas e enums
  services/
    probe_service.py lógica de negócio e erros de domínio
  storage/
    memory.py        armazenamento em memória
tests/
  test_launch.py
  test_movement.py
  test_status.py
```
