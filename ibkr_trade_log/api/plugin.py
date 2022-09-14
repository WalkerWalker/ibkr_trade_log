from datetime import datetime
from typing import Optional

import uvicorn
from starlette.requests import Request
from starlette.responses import RedirectResponse

from fastapi import FastAPI

from bootstrap.logger import LoggerMixin
from ibkr_trade_log.flex.handler import (
    QueryAndStoreReport,
    LoadAndStoreReport,
    OrdersInTimeRange,
)
from ibkr_trade_log.portfolio.handler import CalculatePortfolio


class ApiPlugin(LoggerMixin):
    def __init__(self, app):
        self.api = FastAPI()
        self.app = app
        self.messagebus = self.app.messagebus
        self._load_api()

    def serve(self):
        uvicorn.run(self.api, host="0.0.0.0", log_config=self.logger_config)

    def _load_api(self):
        @self.api.on_event("startup")
        async def startup():  # pragma: no cover
            await self.app.startup()

        @self.api.get("/", include_in_schema=False)
        async def root(request: Request):  # pragma: no cover
            return RedirectResponse(
                request.scope.get("root_path").rstrip("/") + "/docs"
            )

        @self.api.post("/flex_report/load_and_store")
        def load_and_store(filename: str):
            self.messagebus.tell(
                LoadAndStoreReport(
                    filename=filename,
                ),
            )

        @self.api.post("/flex_report/query_and_store")
        def query_and_store():
            self.messagebus.tell(
                QueryAndStoreReport(),
            )

        @self.api.post("/events/orders")
        def orders(before: Optional[datetime] = None, after: Optional[datetime] = None):
            orders_in_time_range = self.messagebus.ask(OrdersInTimeRange(before, after))
            return len(orders_in_time_range)

        @self.api.post("/portfolio/calculate")
        def portfolio_calculate():
            self.messagebus.tell(CalculatePortfolio())
