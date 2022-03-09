from dataclasses import dataclass
from typing import List, Optional

from ib_insync import (
    ContractDetails,
    PortfolioItem,
    Contract,
    ComboLeg,
    Order,
    TagValue,
)

from util import find_gcd


@dataclass
class DetailPortfolioItem:
    contract_details: ContractDetails
    contract: Contract
    position: float
    marketPrice: float
    marketValue: float
    averageCost: float
    unrealizedPNL: float
    realizedPNL: float
    account: str

    @staticmethod
    def append_details(
        contract_details: ContractDetails, portfolio_item: PortfolioItem
    ):
        # TODO change contract to a more detailed version
        new_item = portfolio_item._replace(
            contract=contract_details.contract,
        )
        return DetailPortfolioItem(
            contract_details=contract_details,
            **new_item._asdict(),
        )


@dataclass
class Combo:
    legs: List[DetailPortfolioItem]
    initial_margin: Optional[float] = None
    maintenance_margin: Optional[float] = None

    @property
    def symbol(self):
        return self.legs[0].contract.symbol

    @property
    def currency(self):
        return self.legs[0].contract.currency

    @property
    def exchange(self):
        if len(self.legs) == 1:
            return self.legs[0].contract.exchange
        else:
            return "SMART"

    @property
    def position(self):
        if len(self.legs) == 1:
            return self.legs[0].position

        gcd = find_gcd([int(item.position) for item in self.legs])
        return float(gcd)

    @property
    def contract(self):
        if len(self.legs) == 1:
            return self.legs[0].contract

        combo_leg_list = []
        for leg in self.legs:
            combo_leg_list.append(
                ComboLeg(
                    conId=leg.contract.conId,
                    ratio=int(abs(leg.position) / self.position),
                    action="SELL" if leg.position < 0 else "BUY",
                    exchange=leg.contract.exchange,
                    openClose=0,
                )
            )

        return Contract(
            symbol=self.symbol,
            secType="BAG",
            exchange=self.exchange,
            comboLegs=combo_leg_list,
            currency=self.currency,
        )

    @property
    def what_if_mkt_close_order(self):
        if len(self.legs) == 1:
            position = self.legs[0]
            return Order(
                action="BUY" if position.position < 0 else "SELL",
                totalQuantity=abs(position.position),
                orderType="MKT",
                whatIf=True,
            )
        elif len(self.legs) == 2:
            return Order(
                action="SELL",
                totalQuantity=self.position,
                orderType="MKT",
                whatIf=True,
                smartComboRoutingParams=[
                    TagValue(tag="NonGuaranteed", value="1"),
                ],
            )
        else:  # TODO more than 2 legs, the order must be guaranteed
            return Order(
                action="SELL",
                totalQuantity=self.position,
                orderType="MKT",
                whatIf=True,
            )
