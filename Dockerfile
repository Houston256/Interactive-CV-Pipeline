# Keep external images as explicit stages so Dependabot can update their tags
# and multi-platform index digests.
FROM ghcr.io/astral-sh/uv:0.13.1@sha256:4a1f3666816dafadd20ceb71eac9a7d56d7ef30279f7d64048519ab901ada336 AS uv

FROM python:3.14-slim@sha256:a2b82f3c48559aa0a8446d9af49826b6e2b2016f4cd2afabfe6013ec53729170

WORKDIR /app

COPY --from=uv /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MPLBACKEND=Agg \
    MPLCONFIGDIR=/tmp/mpl \
    HOME=/tmp

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy only runtime files so a future ignore-file mistake cannot include secrets.
COPY .streamlit ./.streamlit
COPY config.toml ./
COPY src ./src

# Run as non-root, /app not writable.
RUN groupadd --gid 10001 app \
    && useradd --uid 10001 --gid 10001 --no-create-home --no-log-init --shell /usr/sbin/nologin app \
    && chown -R root:root /app && chmod -R a-w /app
USER 10001:10001

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD [".venv/bin/python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8501/_stcore/health', timeout=2)"]

# Exec directly so signals reach Streamlit and environment values cannot alter the command.
CMD [".venv/bin/python", "-m", "src.server"]
