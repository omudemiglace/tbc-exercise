FROM python:3.14.5-trixie AS base

# Astral公式イメージから uv および uvx のバイナリをコピー
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Pythonおよびuvの環境変数設定
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /workspace

# 開発環境用ステージ
FROM base AS development

# 本番環境用ステージ
FROM base AS production

USER python
COPY --chown=python:python pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# ソースコードのコピー
COPY --chown=python:python . .
CMD ["uv", "run", "python", "main.py"]