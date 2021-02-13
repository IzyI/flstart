from faker import Faker
import click

from main.database import db
from main.user.models import User
from werkzeug.security import generate_password_hash


@click.option('-n', help='Name user', required=True, )
@click.option('-e', help='Email user', required=True, )
@click.option('-p', help='Password user', required=True, )
def create_user(n, e, p):
    User.create(
        username=n,
        email=e,
        password_hash=generate_password_hash(p),
    )


def create_db():
    """Creates the database."""
    db.create_all()


def drop_db():
    """Drops the database."""
    if click.confirm('Are you sure?', abort=True):
        db.drop_all()


def recreate_db():
    """Same as running drop_db() and create_db()."""
    drop_db()
