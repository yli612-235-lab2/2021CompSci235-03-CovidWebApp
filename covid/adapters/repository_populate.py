from pathlib import Path

from covid.adapters.repository import AbstractRepository
from covid.adapters.csv_data_importer import load_books_and_authors, load_users, load_comments



def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):

    # Load articles and tags into the repository.
    load_books_and_authors(data_path, repo, database_mode)

    # Load users into the repository.
    users = load_users(data_path, repo)

    # Load comments into the repository.
    load_comments(data_path, repo, users)

