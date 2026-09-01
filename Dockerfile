# Keep external images as explicit stages so Dependabot can update their tags
# and multi-platform index digests.
FROM ghcr.io/astral-sh/uv:0.12.9@sha256:8b940d3a9d65bed080436972241af2e21c84b5e8c9193f7014ed71479ee795ff AS uv

FROM python:3.14-slim@sha256:656d12e70054d5fda18a045e2494c96701e9792dd1445f95b3d038df954f57e9

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
