from pathlib import Path

import uvicorn
from ib_insync import FlexReport
from starlette.requests import Request
from starlette.responses import RedirectResponse

from flex.handler import flex, StoreReport
from fastapi import FastAPI

from messagebus.bus import MessageBus


class ApiPlugin:
    def __init__(self, messagebus: MessageBus):
        self.api = FastAPI()
        self.messagebus = messagebus
        self._load_api()

    def startup(self):
        uvicorn.run(self.api)

    def _load_api(self):
        @self.api.get("/", include_in_schema=False)
        async def root(request: Request):  # pragma: no cover
            return RedirectResponse(
                request.scope.get("root_path").rstrip("/") + "/docs"
            )

        @self.api.get("/flex_report/load")
        def load(filename: str, topic: str):
            report_path = Path("reports") / filename
            report = FlexReport(
                path=report_path,
            )

            self.messagebus.tell(
                StoreReport(
                    report=report,
                    topic=topic,
                ),
            )