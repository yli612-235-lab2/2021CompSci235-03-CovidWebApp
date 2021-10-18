import pytest
from sqlalchemy import select, inspect

from covid import metadata


def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)

    assert inspector.get_table_names() == ['authors', 'book_authors', 'books', 'comments', 'popularshelves', 'users']


def test_database_populate_select_all_authors(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_authors_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        # query for records in table tags
        select_statement = select([metadata.tables[name_of_authors_table]])
        result = connection.execute(select_statement)

        all_author_names = []
        for row in result:
            all_author_names.append(row['author_name'])

        assert all_author_names == ['Lindsey Schussman', 'Florence Dupre la Tour', 'Ed Brubaker',
                                    'Jason Delgado', 'Chris  Martin', 'Jerry Siegel', 'Joe Shuster',
                                    'Yuu Asami', 'Garth Ennis', 'Tomas Aira', 'Keith Burns',
                                    'Matt Martin', 'Mike Wolfer', 'Simon Spurrier',
                                    'Fernando Heinz', 'Rafael Ortiz', 'DigiKore Studios',
                                    'Jaymes Reed', 'Jeon Geuk-Jin', 'Scott Beatty',
                                    'Daniel Indro', 'Naoki Urasawa', 'Rich Tommaso', 'Maki Minami',
                                    'Takashi   Murakami', 'Cun Shang Chong', 'Asma', 'Dan Slott', 'Andrea DiVito',
                                    'Kieron Dwyer', 'Katsura Hoshino']

def test_database_populate_select_all_users(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_name'])

        assert all_users == ['thorke', 'fmercury', 'mjackson', 'MyTest']

def test_database_populate_select_all_comments(database_engine):

    # Get table information
    inspector = inspect(database_engine)

    name_of_comments_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        # query for records in table comments
        select_statement = select([metadata.tables[name_of_comments_table]])

        result = connection.execute(select_statement)

        all_comments = []
        for row in result:

            all_comments.append((row['id'], row['user_id'], row['book_id'], row['comment']))

        assert all_comments == [(1, 2, 25742454, 'Oh ,good'),
                                (2, 1, 25742454, 'Yeah good news'),
                                (3, 3, 25742454, 'Ha ha ha!'),
                                (4, 3, 13571772, 'cxvgdfgf'),
                                (5, 3, 25742454, 'cffxdscdxz')]



def test_database_populate_select_all_books(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_books_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_books_table]])
        result = connection.execute(select_statement)

        all_books = []
        for row in result:
            all_books.append((row['id'], row['title']))

        nr_books = len(all_books)

        assert nr_books == 20
        assert all_books[0] == (1, 'The Switchblade Mamma')

if __name__ == '__main__':
    pytest.main(["-s", "test_populate_database.py"])