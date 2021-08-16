"""Flask configuration variables."""
from os import environ
from dotenv import load_dotenv

from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent


# Load environment variables from file .env, stored in this directory.
load_dotenv()


class Config:
    """Set Flask configuration from .env file."""

    # Flask configuration
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    SECRET_KEY = environ.get('SECRET_KEY')

