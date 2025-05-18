FROM python:3.11 as requirements-stage

ENV POETRY_VERSION=2.1.3

WORKDIR /tmp

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && pip install poetry-plugin-export

COPY ./pyproject.toml /tmp/

RUN poetry lock

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11

WORKDIR /app

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app/app

COPY pyproject.toml /app/

COPY ./alembic.ini .

COPY ./compose/local/fastapi/start.sh .
RUN chmod +x /app/start.sh
