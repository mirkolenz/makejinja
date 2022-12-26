ARG POETRY_VERSION=1.3.1
ARG PYTHON_VERSION=3.9

FROM python:${PYTHON_VERSION}-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV args="--help"

WORKDIR /app

RUN apt update && \
    apt install -y curl && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:${PATH}"
RUN curl -sSL https://install.python-poetry.org | python -

COPY poetry.lock* pyproject.toml ./
RUN poetry install --no-interaction --no-ansi --no-root
COPY makejinja ./makejinja

CMD [ "sh", "-c", "poetry run python -m makejinja ${args}" ]
