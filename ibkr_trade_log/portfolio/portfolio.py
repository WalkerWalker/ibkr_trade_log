from typing import List, Dict

from bootstrap.ddd import Entity
from ibkr_trade_log.portfolio.campaign import Campaign


class Portfolio(Entity):
    cash: Dict[str, int] = {}
    campaigns: Dict[str, List[Campaign]] = {}
