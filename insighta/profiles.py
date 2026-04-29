# insighta/profiles.py
import typer
from rich.console import Console
from rich.table import Table

from insighta.client import api_get

profiles_app = typer.Typer()
console = Console()


@profiles_app.command("list")
def list_profiles(
    gender: str = None,
    country: str = None,
    age_group: str = None,
    min_age: int = None,
    max_age: int = None,
    sort_by: str = "created_at",
    order: str = "desc",
    page: int = 1,
    limit: int = 10
):
    params = {
        "gender": gender,
        "country_id": country,
        "age_group": age_group,
        "min_age": min_age,
        "max_age": max_age,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
    }

    with console.status("[bold green]Fetching profiles..."):
        response = api_get("/api/profiles", params=params)

    data = response.json()

    if response.status_code != 200:
        console.print(data)
        raise typer.Exit()

    table = Table(title="Profiles")

    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Gender")
    table.add_column("Age")
    table.add_column("Country")

    for p in data["data"]:
        table.add_row(
            p["id"],
            p["name"],
            p["gender"],
            str(p["age"]),
            p["country_id"]
        )

    console.print(table)


@profiles_app.command("get")
def get_profile(profile_id: str):

    with console.status("[bold green]Fetching profile..."):
        response = api_get(f"/api/profiles/{profile_id}")

    data = response.json()

    if response.status_code != 200:
        console.print(data)
        raise typer.Exit()

    console.print(data)


from insighta.client import api_post


@profiles_app.command("create")
def create_profile(name: str):

    with console.status("[bold green]Creating profile..."):
        response = api_post(
            "/api/profiles",
            json={"name": name}
        )

    data = response.json()

    if response.status_code not in [200, 201]:
        console.print(data)
        raise typer.Exit()

    console.print(data)


@profiles_app.command("search")
def search_profiles(query: str):

    with console.status("[bold green]Searching profiles..."):
        response = api_get(
            "/api/profiles/search",
            params={"q": query}
        )

    data = response.json()

    if response.status_code != 200:
        console.print(data)
        raise typer.Exit()

    table = Table(title="Search Results")

    table.add_column("Name")
    table.add_column("Gender")
    table.add_column("Age")
    table.add_column("Country")

    for p in data["data"]:
        table.add_row(
            p["name"],
            p["gender"],
            str(p["age"]),
            p["country_id"]
        )

    console.print(table)
