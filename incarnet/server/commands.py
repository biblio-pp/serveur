import click
from incarnet.server import app, db
from incarnet.server.models import User
from flask.cli import AppGroup

user_cli = AppGroup("user")

@user_cli.command("create")
@click.option("--username", prompt="Username", help="Sets the username.")
@click.option(
    "--password",
    prompt="Password",
    hide_input=True,
    help="Sets the user's password (for security, avoid setting this from the command line).",
)
def create_user(username, password):
    """Create a user directly in the database."""
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
    else:
        raise KeyError(f"User '{username}' already exists.")


@user_cli.command("delete")
@click.argument("username")
@click.option(
    "--yes",
    is_flag=True,
    expose_value=False,
    prompt=f"Are you sure you want to delete this user?",
)
def delete_user(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        raise KeyError(f"User {username} does not exist.")
    else:
        db.session.delete(user)
        db.session.commit()


app.cli.add_command(user_cli)
