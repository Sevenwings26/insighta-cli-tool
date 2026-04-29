# insighta/client.py
import httpx
import typer

from insighta.config import (
    API_BASE_URL,
    load_credentials,
    save_credentials,
    clear_credentials,
)

console = typer.secho


def refresh_access_token():
    creds = load_credentials()

    if not creds:
        return None

    refresh_token = creds.get("refresh_token")

    if not refresh_token:
        return None

    response = httpx.post(
        f"{API_BASE_URL}/auth/refresh",
        json={"refresh_token": refresh_token},
        headers={"X-API-Version": "1"},
    )

    if response.status_code != 200:
        clear_credentials()
        return None

    data = response.json()

    save_credentials({
        "access_token": data["access_token"],
        "refresh_token": data["refresh_token"],
    })

    return data["access_token"]


def get_headers():
    creds = load_credentials()

    headers = {
        "X-API-Version": "1"
    }

    if creds and creds.get("access_token"):
        headers["Authorization"] = (
            f"Bearer {creds['access_token']}"
        )

    return headers


def handle_auth_failure():
    new_token = refresh_access_token()

    if not new_token:
        typer.echo("Session expired. Please login again.")
        raise typer.Exit(code=1)


def request(method, path, **kwargs):
    response = httpx.request(
        method,
        f"{API_BASE_URL}{path}",
        headers=get_headers(),
        **kwargs
    )

    if response.status_code == 401:
        handle_auth_failure()

        response = httpx.request(
            method,
            f"{API_BASE_URL}{path}",
            headers=get_headers(),
            **kwargs
        )

    return response


def api_get(path, params=None):
    return request("GET", path, params=params)


def api_post(path, json=None):
    return request("POST", path, json=json)


def api_delete(path):
    return request("DELETE", path)
