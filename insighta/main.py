# insighta/main.py
import typer

from insighta.auth import auth_app
from insighta.profiles import profiles_app
# from insighta.profile_export import profile_export_app
from insighta.profile_export import export_app

profiles_app.add_typer(export_app)


app = typer.Typer()

# routes to sub-apps
app.add_typer(auth_app, name="auth")
app.add_typer(profiles_app, name="profiles")


@app.command()
def login():
    """
    Login via GitHub OAuth
    """
    from insighta.auth import login_user
    login_user()


@app.command()
def logout():
    from insighta.auth import logout_user
    logout_user()


@app.command()
def whoami():
    from insighta.auth import whoami_user
    whoami_user()


if __name__ == "__main__":
    app()

    

# import typer

# app = typer.Typer(help="A simple CLI app that greets users.")

# @app.command()
# def greet(
#     name: str = typer.Argument('Iyanu', help="The name of the person to greet"),
#     times: int = typer.Option(1, help="Number of times to greet"),
#     excited: bool = typer.Option(False, help="Add excitement to the greeting")
# ):
#     """
#     Greet a user by name.
#     """
#     for _ in range(times):
#         message = f"Hello, {name}"
#         if excited:
#             message += "!!!"
#         typer.echo(message)

# if __name__ == "__main__":
#     app()
