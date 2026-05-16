FROM ghcr.io/astral-sh/uv:0.9.30-python3.12-bookworm AS runtime

WORKDIR /workspace/backend

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --frozen --all-extras --dev

COPY backend/src ./src

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "src.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
