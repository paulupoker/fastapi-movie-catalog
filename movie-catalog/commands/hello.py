from typing import Annotated

import typer
from rich import print

app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.command()
def hello(
    name: Annotated[
        str,
        typer.Argument(help="Name to greet"),
    ],
) -> None:
    """
    Greet user by name
    """
    print(f"[bold]Hello, [green]{name}[/green]![/bold]")
