import yaml

from ibkr_trade_log.app.app import IbkrApp


def main():
    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

    app = IbkrApp(config=config)
    app.cli_plugin.cli()


if __name__ == "__main__":  # pragma: no cover
    main()
