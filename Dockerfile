FROM --platform=linux/amd64 python:3.8-slim-buster

WORKDIR /app
RUN pip install poetry
COPY poetry.lock .
COPY pyproject.toml .
RUN poetry config virtualenvs.create false \
    && poetry install
COPY . .
CMD ["serve"]
ENTRYPOINT ["ibkr-trade-log"]
