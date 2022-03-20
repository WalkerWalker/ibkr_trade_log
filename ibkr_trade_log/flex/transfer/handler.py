from dataclasses import dataclass

from bootstrap.messagebus.handler import Handler
from bootstrap.messagebus.model import Command
from ibkr_trade_log.flex.transfer.repository import TransferDataFrame


@dataclass(frozen=True)
class StoreTransfers(Command):
    transfer_data_frame: TransferDataFrame


class TransferHandler(Handler):
    def __init__(self, messagebus, transfer_repository):
        super().__init__(messagebus)
        self.transfer_repository = transfer_repository

    def startup(self):
        self.messagebus.declare(StoreTransfers, self.handle_transfers)

    def handle_transfers(self, command: StoreTransfers):
        self.transfer_repository.add(
            record_set=command.transfer_data_frame,
        )
