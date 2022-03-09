import typer
from typer import Context

cli = typer.Typer()


@cli.command(help="Serve the fastapi")
def serve(ctx: typer.Context):
    app = ctx.obj
    app.api_plugin.serve()


class CliPlugin:
    def __init__(self, app):
        self.cli = cli

        @cli.callback()
        def context(
            ctx: Context,
        ):
            ctx.obj = app
