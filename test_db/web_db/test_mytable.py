import datetime


import pytest
from sqlalchemy.exc import IntegrityError

from covid.domain.model import User, make_comment, Book, Author, make_author_association


def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_book(empty_session):
    empty_session.execute(
        'INSERT INTO books (book_id, ebook, publication_year, publication_data, title,average_rating,hyperlink,image_hyperlink,publisher,description) VALUES '
        '(:book_id, :ebook, :publication_year, :publication_data, :title, :average_rating, :hyperlink, :image_hyperlink, :publisher, :description)',
        {'book_id': 25742454, 'ebook': True, 'publication_year': 2021, 'publication_data': '2021-01-01.', 'title': 'The Switchblade Mamma',
         'average_rating': '4.12.', 'hyperlink': 'https://www.goodreads.com/book/show/25742454-the-switchblade-mamma',
         'image_hyperlink': 'https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png',
         'publisher': 'Hakusensha', 'description': 'Lillian Ann Cross is forced to live the worst nightmare of her life. She is an everyday middle class American'}
    )


    row = empty_session.execute('SELECT book_id from books').fetchone()

    return row[0]


def insert_authors(empty_session):
    empty_session.execute(
        'INSERT INTO authors (author_id,author_name)  VALUES (:author_id, :author_name)',
                              {'author_id': 2983296, 'author_name': 'Anton Szandor LaVey'})

    empty_session.execute(
        'INSERT INTO authors (author_id,author_name)  VALUES (:author_id, :author_name)',
                              {'author_id': 30000, 'author_name': '3000Anton Szandor LaVey'})

    rows = list(empty_session.execute('SELECT author_id from authors'))

    keys = tuple(row[0] for row in rows)
    return keys



def insert_book_author_associations(empty_session, book_key, author_keys):
    stmt = 'INSERT INTO book_authors (book_id, author_id) VALUES (:book_id, :author_id)'

    for author_key in author_keys:
        empty_session.execute(stmt, {'book_id': book_key, 'author_id': author_key})


def insert_commented_book(empty_session):
    book_key = insert_book(empty_session)
    user_key = insert_user(empty_session)

    timestamp_1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    empty_session.execute(
        'INSERT INTO comments (user_id, book_id, comment, timestamp) VALUES '
        '(:user_id, :book_id, "Comment 1", :timestamp_1),'
        '(:user_id, :book_id, "Comment 2", :timestamp_2)',
        {'user_id': user_key, 'book_id': book_key, 'timestamp_1': timestamp_1, 'timestamp_2': timestamp_2}
    )

    row = empty_session.execute('SELECT book_id from books').fetchone()
    return row[0]

def make_book():
    book =  Book(
        2021,
        '2021-01-01.',
        25742454,
        'The Switchblade Mamma',
        True,
        "https://www.goodreads.com/book/show/25742454-the-switchblade-mamma",
        "https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png",
        "Lillian Ann Cross is forced to live the worst nightmare of her life. She is an everyday middle class American,",
        "Hakusensha",
        '4.12.')
    return book


def make_user():
    user = User("Andrew", "111")
    return user


def make_author():
    author = Author(2983296,"Anton Szandor LaVey")
    return author


def test_loading_of_users(empty_session):
    users = list()
    users.append(("Andrew", "1234"))
    users.append(("Cindy", "1111"))

    insert_users(empty_session, users)

    expected = [
        User("Andrew", "1234"),
        User("Cindy", "999")
    ]
    assert empty_session.query(User).all() == expected

def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [("Andrew", "111")]


def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("Andrew", "1234"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("Andrew", "111")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_book(empty_session):
    book_key = insert_book(empty_session)
    expected_book = make_book()
    fetched_book = empty_session.query(Book).one()
    #
    assert expected_book == fetched_book
    assert book_key == fetched_book.book_id

def test_loading_of_tagged_book(empty_session):
    book_key = insert_book(empty_session)

    author_keys = insert_authors(empty_session)

    insert_book_author_associations(empty_session, book_key, author_keys)
    #
    book = empty_session.query(Book).filter(Book._Book__book_id==book_key).one()

    authors = empty_session.query(Author).filter(Author._Author__author_id.in_(author_keys)).all()

    for auhtor in authors:
        assert book.is_author_by(auhtor)
        assert auhtor.is_applied_to(book)

def test_loading_of_commented_book(empty_session):
    insert_commented_book(empty_session)
    rows = empty_session.query(Book).all()
    book = rows[0]

    for comment in book.comments:
        assert comment.book is book

def test_saving_of_book(empty_session):
    book = make_book()
    empty_session.add(book)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT book_id, ebook, publication_year, publication_data, title,average_rating,hyperlink,image_hyperlink,publisher,description FROM books'))
    assert rows ==[(25742454,
                    1, 2021, '2021-01-01.', 'The Switchblade Mamma',
                    '4.12.',
                    'https://www.goodreads.com/book/show/25742454-the-switchblade-mamma',
                    'https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png',
                    'Hakusensha',
                    'Lillian Ann Cross is forced to live the worst nightmare of her life. She is an everyday middle class American,')]



def test_saving_of_comment(empty_session):
    book_key = insert_book(empty_session)
    user_key = insert_user(empty_session, ("Andrew", "1234"))

    rows = empty_session.query(Book).all()
    book = rows[0]
    user = empty_session.query(User).filter(User._User__user_name == "Andrew").one()

    # Create a new Comment that is bidirectionally linked with the User and Article.
    comment_text = "Some comment text."
    comment = make_comment(comment_text, user, book)

    # Note: if the bidirectional links between the new Comment and the User and
    # Article objects hadn't been established in memory, they would exist following
    # committing the addition of the Comment to the database.
    empty_session.add(comment)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id,book_id, comment FROM comments'))

    assert rows == [(user_key, book_key, comment_text)]

def test_saving_author_book(empty_session):
    book = make_book()
    author = make_author()

    # Establish the bidirectional relationship between the Article and the Tag.
    make_author_association(book, author)

    # Persist the Article (and Tag).
    # Note: it doesn't matter whether we add the Tag or the Article. They are connected
    # bidirectionally, so persisting either one will persist the other.
    empty_session.add(book)
    empty_session.commit()

    # Test test_saving_of_article() checks for insertion into the articles table.
    rows = list(empty_session.execute('SELECT book_id FROM books'))
    book_key = rows[0][0]

    # Check that the tags table has a new record.
    rows = list(empty_session.execute('SELECT author_id, author_name FROM authors'))
    author_key = rows[0][0]

    assert rows[0][1] == "Anton Szandor LaVey"

    # Check that the article_tags table has a new record.
    rows = list(empty_session.execute('SELECT book_id, author_id from book_authors'))
    book_foreign_key = rows[0][0]
    author_foreign_key = rows[0][1]

    assert book_key == book_foreign_key
    assert author_key == author_foreign_key


def test_save_commented_book(empty_session):
    # Create Article User objects.
    book = make_book()
    user = make_user()

    # Create a new Comment that is bidirectionally linked with the User and Article.
    comment_text = "Some comment text."
    comment = make_comment(comment_text, user, book)

    # Save the new Article.
    empty_session.add(book)
    empty_session.commit()

    # Test test_saving_of_article() checks for insertion into the articles table.
    rows = list(empty_session.execute('SELECT book_id FROM books'))
    book_key = rows[0][0]

    # Test test_saving_of_users() checks for insertion into the users table.
    rows = list(empty_session.execute('SELECT id FROM users'))
    user_key = rows[0][0]

    # Check that the comments table has a new record that links to the articles and users
    # tables.
    rows = list(empty_session.execute('SELECT user_id, book_id, comment FROM comments'))
    assert rows == [(user_key, book_key, comment_text)]