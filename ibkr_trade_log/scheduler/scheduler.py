import asyncio
from asyncio import AbstractEventLoop
from datetime import timedelta
from typing import Optional, Callable

from rx import timer
from rx.scheduler.eventloop import AsyncIOScheduler


class Scheduler:
    def __init__(self):
        self.main_loop: Optional[AbstractEventLoop] = None
        self.aio_scheduler: Optional[AsyncIOScheduler] = None

    def startup(self):
        self.main_loop = asyncio.get_running_loop()
        self.aio_scheduler = AsyncIOScheduler(self.main_loop)

    def schedule(self, duetime: timedelta, period: timedelta, callback: Callable):
        def on_next(_):
            callback()

        return timer(
            duetime=duetime.total_seconds(),
            period=period.total_seconds(),
            scheduler=self.aio_scheduler,
        ).subscribe(
            on_next=on_next,
        )
