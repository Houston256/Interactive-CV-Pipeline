FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

EXPOSE ${PORT}

HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT}/_stcore/health')" || exit 1

CMD uv run python -m streamlit run src/main.py --server.port=${PORT} --server.address=0.0.0.0
