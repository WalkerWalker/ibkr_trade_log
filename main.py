import yaml

import order
from api.plugin import ApiPlugin
from flex.handler import FlexHandler, FlexConfig
from messagebus.memory import MemoryMessageBus
from rdb.config import RdbConfig
from rdb.session import RdbSessionFactory

with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

# messagebus plugin startup
messagebus = MemoryMessageBus()

# rdb plugin startup
rdb_config = RdbConfig(**config["rdb"])
rdb_session_factory = RdbSessionFactory(config=rdb_config)
rdb_session_factory.startup()

# flex handler
flex_config = FlexConfig(**config["flex"])
flex_handler = FlexHandler(messagebus=messagebus, config=flex_config)
flex_handler.startup()

# order
order.startup(
    rdb_session_factory=rdb_session_factory,
    messagebus=messagebus,
)

# api plugin startup
api_plugin = ApiPlugin(messagebus=messagebus)
api_plugin.startup()
