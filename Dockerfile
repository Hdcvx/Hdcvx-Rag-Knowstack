FROM python:3.12-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project

COPY . .

CMD ["uv", "run", "--frozen", "python", "main.py"]
