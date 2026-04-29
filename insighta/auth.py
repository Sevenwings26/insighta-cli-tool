# insighta/auth.py

import webbrowser
import typer
import httpx

from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
)

from insighta.config import (
    save_credentials,
    load_credentials,
    clear_credentials,
    API_BASE_URL,
)

auth_app = typer.Typer()
console = Console()


# -----------------------------------
# LOGIN
# -----------------------------------
@auth_app.command("login")
def login_user():
    """
    Login via GitHub OAuth
    """

    login_url = f"{API_BASE_URL}/auth/github"

    console.print(
        Panel.fit(
            "[bold green]Opening GitHub login...[/bold green]"
        )
    )

    webbrowser.open(login_url)

    typer.echo(
        "\nAfter login, copy the tokens returned "
        "from the callback response.\n"
    )

    access_token = typer.prompt("Access Token")
    refresh_token = typer.prompt("Refresh Token")

    save_credentials({
        "access_token": access_token,
        "refresh_token": refresh_token
    })

    console.print(
        "[green]Login successful.[/green]"
    )


# -----------------------------------
# LOGOUT
# -----------------------------------
@auth_app.command("logout")
def logout_user():
    """
    Logout and revoke refresh token
    """

    creds = load_credentials()

    if not creds:
        console.print(
            "[yellow]Already logged out.[/yellow]"
        )
        return

    refresh_token = creds.get("refresh_token")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}")
    ) as progress:

        progress.add_task(
            description="Logging out...",
            total=None
        )

        response = httpx.post(
            f"{API_BASE_URL}/auth/logout",
            json={
                "refresh_token": refresh_token
            },
            headers={
                "X-API-Version": "1"
            }
        )

    clear_credentials()

    if response.status_code == 200:
        console.print(
            "[green]Logout successful.[/green]"
        )
    else:
        console.print(
            "[red]Logout failed.[/red]"
        )


# -----------------------------------
# WHOAMI
# -----------------------------------
@auth_app.command("whoami")
def whoami_user():
    """
    Show current authenticated user
    """

    creds = load_credentials()

    if not creds:
        console.print(
            "[red]Not logged in.[/red]"
        )
        raise typer.Exit(code=1)

    headers = {
        "Authorization": (
            f"Bearer {creds['access_token']}"
        ),
        "X-API-Version": "1"
    }

    with console.status(
        "[bold green]Fetching user...[/bold green]"
    ):
        response = httpx.get(
            f"{API_BASE_URL}/auth/me",
            headers=headers
        )

    if response.status_code == 401:
        console.print(
            "[red]Session expired. Please login again.[/red]"
        )
        clear_credentials()
        raise typer.Exit(code=1)

    if response.status_code != 200:
        console.print(response.text)
        raise typer.Exit(code=1)

    data = response.json()

    console.print(
        Panel.fit(
            f"""
[bold]Username:[/bold] {data.get("username")}
[bold]Email:[/bold] {data.get("email")}
[bold]Role:[/bold] {data.get("role")}
"""
        )
    )
    