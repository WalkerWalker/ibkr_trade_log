FROM --platform=linux/amd64 python:3.8-slim-buster

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only main
COPY bootstrap ./bootstrap
COPY ibkr_trade_log ./ibkr_trade_log
RUN poetry install --only main
CMD ["serve"]
ENTRYPOINT ["ibkr-trade-log"]
