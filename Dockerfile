FROM --platform=linux/amd64 python:3.8-slim-buster

WORKDIR /app
RUN pip install poetry
COPY . .
RUN poetry config virtualenvs.create false \
    && poetry install
CMD ["serve"]
ENTRYPOINT ["ibkr-trade-log"]
