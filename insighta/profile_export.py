# insighta/profile_export.py
import os
import typer

from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
)

from insighta.client import api_get

export_app = typer.Typer()
console = Console()


@export_app.command("export")
def export_profiles(
    format: str = typer.Option("csv"),
    gender: str = typer.Option(None),
    country: str = typer.Option(None),
    age_group: str = typer.Option(None),
    min_age: int = typer.Option(None),
    max_age: int = typer.Option(None),
    sort_by: str = typer.Option("created_at"),
    order: str = typer.Option("desc"),
):

    params = {
        "format": format,
        "gender": gender,
        "country_id": country,
        "age_group": age_group,
        "min_age": min_age,
        "max_age": max_age,
        "sort_by": sort_by,
        "order": order,
    }

    params = {
        k: v for k, v in params.items()
        if v is not None
    }

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}")
    ) as progress:

        progress.add_task(
            description="Exporting profiles...",
            total=None
        )

        response = api_get(
            "/api/profiles/export",
            params=params
        )

    if response.status_code != 200:
        console.print(
            f"[red]Export failed:[/red] {response.text}"
        )
        raise typer.Exit(code=1)

    filename = f"profiles_export.{format}"

    with open(filename, "wb") as f:
        f.write(response.content)

    console.print(
        f"[green]Saved:[/green] {os.path.abspath(filename)}"
    )