from ib_insync import IB

from portfolio import Portfolio


def main():
    ib = IB()
    ib.connect(
        host="127.0.0.1",
        port=7496,
        clientId=0,
    )
    portfolio_items = ib.portfolio()
    portfolio = Portfolio(portfolio_items=portfolio_items, ib=ib)
    portfolio.request_contract_details()
    portfolio.generate_combos()
    portfolio.request_combo_margin()
    total_maintenance_margin = 0
    total_initial_margin = 0
    for combo in portfolio.combos:
        total_maintenance_margin += combo.maintenance_margin
        total_initial_margin += combo.initial_margin
    print(total_maintenance_margin)
    print(total_initial_margin)
    ib.disconnect()


if __name__ == "__main__":
    main()
