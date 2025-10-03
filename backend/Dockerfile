FROM python:3.12

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY uv.lock pyproject.toml ./

RUN uv sync --locked --no-dev

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . .

CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "project.wsgi"]