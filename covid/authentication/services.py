from pathlib import Path

from werkzeug.security import generate_password_hash, check_password_hash

from covid.adapters.csv_data_importer import write_csv_file
from covid.adapters.repository import AbstractRepository
from covid.domain.model import User


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


def write_user(user_name: str, password: str, repo: AbstractRepository):
    my_user = []
    my_user.append(repo.get_number_of_user())
    my_user.append(user_name)
    my_user.append(password)

    data_path = Path('MyWeb') / 'adapters' / 'data'
    users_filename = str(Path(data_path) / "users.csv")
    write_csv_file(users_filename, my_user)


# def sql_write_user(user_name: str, password: str, repo: AbstractRepository):
#     add_sql_users(repo.get_number_of_user(),user_name,password)

def add_user(user_name: str, password: str, repo: AbstractRepository):
    # Check that the given user name is available.
    user = repo.get_user(user_name)
    if user is not None:
        raise NameNotUniqueException

    # Encrypt password so that the database doesn't store passwords 'in the clear'.
    password_hash = generate_password_hash(password)

    # Create and store the new User, with password encrypted.
    user = User(user_name, password_hash)

    repo.add_user(user)


def get_user(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    return user_to_dict(user)


def authenticate_user(user_name: str, password: str, repo: AbstractRepository):
    authenticated = False

    user = repo.get_user(user_name)
    if user is not None:
        authenticated = check_password_hash(user.password, password)
    if not authenticated:
        raise AuthenticationException


# ===================================================
# Functions to convert model entities to dictionaries
# ===================================================

def user_to_dict(user: User):
    user_dict = {
        'user_name': user.user_name,
        'password': user.password
    }
    return user_dict
