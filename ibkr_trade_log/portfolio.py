from typing import List

from ib_insync import PortfolioItem, IB

from ibkr_trade_log.model import DetailPortfolioItem, Combo


def get_margin_report(ib):
    portfolio_items = ib.portfolio()
    portfolio = Portfolio(portfolio_items=portfolio_items, ib=ib)
    portfolio.request_contract_details()
    portfolio.generate_combos()
    portfolio.request_combo_margin()
    total = sum([combo.maintenance_margin for combo in portfolio.combos])
    for combo in portfolio.combos:
        print(
            combo.symbol,
            combo.maintenance_margin,
            combo.maintenance_margin / total * 100,
        )


class Portfolio:
    def __init__(self, portfolio_items: List[PortfolioItem], ib: IB):
        self.ib = ib
        self.portfolio_items = portfolio_items
        self.detail_portfolio_items = None
        self.combos = None

    def request_contract_details(self):
        detail_portfolio_items = []
        for item in self.portfolio_items:
            contract_details_list = self.ib.reqContractDetails(
                contract=item.contract,
            )
            if len(contract_details_list) > 0:
                detail_portfolio_items.append(
                    DetailPortfolioItem.append_details(
                        contract_details=contract_details_list[0],
                        portfolio_item=item,
                    ),
                )
        self.detail_portfolio_items = detail_portfolio_items

    def generate_combos(self):
        combo_dict = {}
        for item in self.detail_portfolio_items:
            symbol = item.contract.symbol
            if symbol not in combo_dict:
                combo_dict[symbol] = []
            combo_dict[symbol].append(item)

        combos = []
        for symbol in combo_dict:
            combos.append(
                Combo(
                    legs=combo_dict[symbol],
                )
            )

        self.combos = combos

    def request_combo_margin(self):
        for combo in self.combos:
            contract = combo.contract
            order = combo.what_if_mkt_close_order
            order_state = self.ib.whatIfOrder(
                contract=contract,
                order=order,
            )
            combo.initial_margin = -float(order_state.initMarginChange)
            combo.maintenance_margin = -float(order_state.maintMarginChange)

    def write_to_google(self):
        pass
