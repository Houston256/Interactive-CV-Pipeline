# Interactive CV Pipeline

## Local

```console
uv sync
uv run python -m streamlit run src/main.py
uv run pytest
```

## Docker

```console
docker compose up --build -d --wait
```

On the VPS, you can run the Compose file directly from GitHub; no local copy is
needed. The Compose file pulls the published image from GHCR:

```console
docker compose \
  -f https://github.com/Houston256/Interactive-CV-Pipeline.git#main:docker-compose.yml \
  up -d --pull always --no-build --wait
```

