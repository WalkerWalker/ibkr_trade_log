import asyncio

import yaml

import order
from api.plugin import ApiPlugin
from app.app import IbkrApp
from flex.handler import FlexHandler, FlexConfig
from messagebus.memory import MemoryMessageBus
from rdb.config import RdbConfig
from rdb.session import RdbSessionFactory


def main():
    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

    app = IbkrApp(config=config)
    app.api_plugin.serve()


if __name__ == "__main__":
    main()
