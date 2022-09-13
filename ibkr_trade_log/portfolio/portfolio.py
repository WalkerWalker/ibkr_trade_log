from bootstrap.ddd import Entity


class Portfolio(Entity):
    cash: dict = {}
    campaigns: dict = {}
