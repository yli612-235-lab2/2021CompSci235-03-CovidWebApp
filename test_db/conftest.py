import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from covid import metadata, map_model_to_tables
from covid.adapters import database_repository, repository_populate
from utils import get_project_root

TEST_DATA_PATH_DATABASE_FULL = get_project_root() / "covid" / "adapters" / "data"
TEST_DATA_PATH_DATABASE_LIMITED = get_project_root() / "tests" / "data"

TEST_DATABASE_URI_IN_MEMORY = 'sqlite:///em.db'
TEST_DATABASE_URI_FILE = 'sqlite:///mytest.db'

@pytest.fixture
def database_engine():
    engine = create_engine(TEST_DATABASE_URI_FILE)
    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)

    if len(engine.table_names()) == 0:
        clear_mappers()
        metadata.create_all(engine)  # Conditionally create database tables.
        for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
            engine.execute(table.delete())

        map_model_to_tables()

        database_mode = True
        repository_populate.populate(TEST_DATA_PATH_DATABASE_LIMITED, repo_instance, database_mode)
    else:
        map_model_to_tables()

    yield engine
    # metadata.drop_all(engine)

@pytest.fixture
def session_factory():
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)

    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)

    if len(engine.table_names()) == 0:
        clear_mappers()
        metadata.create_all(engine)
        for table in reversed(metadata.sorted_tables):
            engine.execute(table.delete())
        map_model_to_tables()

        database_mode = True
        repository_populate.populate(TEST_DATA_PATH_DATABASE_FULL, repo_instance, database_mode)
    else:
        map_model_to_tables()
    yield session_factory
    # metadata.drop_all(engine)

@pytest.fixture
def empty_session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    # metadata.drop_all(engine)

if __name__ == '__main__':
    pytest.main(["-s", "conftest.py"])