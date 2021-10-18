from datetime import date

import pytest

from covid.adapters.database_repository import SqlAlchemyRepository
from covid.domain.model import User, Book, make_comment


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('Dave')

    assert user2 == user and user2 is user

def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')

def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('prince')
    assert user is None

def test_repository_can_retrieve_book_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_books = repo.get_number_of_books()

    assert number_of_books == 20

def test_repository_can_add_article(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_books = repo.get_number_of_books()

    new_book_id = number_of_books + 1

    book =  Book(
        2020,
        '2020-03-09',
        new_book_id,
        'Second US coronavirus cruise tests negative amid delays and cancellations',
        True,
        'https://www.nzherald.co.nz/travel/news/article.cfm?c_id=7&objectid=12315024',
        'https://www.nzherald.co.nz/resizer/ix7hy3lzkMWUkD8hE6kdZ-8oaOM=/620x349/smart/filters:quality(70)/arc-anglerfish-syd-prod-nzme.s3.amazonaws.com/public/7VFOBLCBCNDHLICBY3CTPFR2L4.jpg',
        "Lillian Ann Cross is forced to live the worst nightmare of her life. She is an everyday middle class American,",
        "Hakusensha",
        '4.12.')

    repo.add_book(book)

    assert repo.get_book(new_book_id) == book

def test_repository_does_not_retrieve_a_non_existent_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    #25742454
    book = repo.get_book(257)
    assert book is None

def test_repository_can_retrieve_books_by_date(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    books = repo.get_books_by_publication_year(2021)

    assert len(books) == 4



def test_repository_does_not_retrieve_an_book_when_there_are_no_books_for_a_given_date(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # # these articles are no jokes...
    books = repo.get_books_by_publication_year(1991)   #

    assert len(books) == 0

def test_repository_can_retrieve_tags(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    authors = repo.get_authors()

    assert len(authors) == 31
    #
    author_one = [author for author in authors if author.author_name == 'Lindsey Schussman'][0]
    author_two = [author for author in authors if author.author_name == 'Chris  Martin'][0]
    author_three = [author for author in authors if author.author_name == 'Matt Martin'][0]
    author_four = [author for author in authors if author.author_name == 'Andrea DiVito'][0]

    assert author_one.number_of_author_books == 1
    assert author_two.number_of_author_books == 1
    assert author_three.number_of_author_books == 1
    assert author_four.number_of_author_books == 1

def test_repository_can_get_first_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = repo.get_first_book()
    print(book.title)
    assert book.title == 'The Switchblade Mamma'

def test_repository_can_get_last_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = repo.get_last_book()

    print(book.title)
    assert book.title == 'Bounty Hunter 4/3: My Life in Combat from Marine Scout Sniper to MARSOC'

def test_repository_can_get_articles_by_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    books = repo.get_books_by_id([2250580, 27036538, 13571772])

    assert len(books) == 3
    assert books[0].title == 'Captain America: Winter Soldier (The Ultimate Graphic Novels Collection: Publication Order, #7)'
    assert books[1].title == "A.I. Revolution, Vol. 1"
    assert books[2].title == 'Crossed + One Hundred, Volume 2 (Crossed +100 #2)'

def test_repository_does_not_retrieve_book_for_non_existent_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    books = repo.get_books_by_id([2250580, 9])

    assert len(books) == 1

    assert books[0].title == 'A.I. Revolution, Vol. 1'

def test_repository_returns_an_empty_list_for_non_existent_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    books = repo.get_books_by_id([0, 199])

    assert len(books) == 0

def test_repository_returns_an_empty_list_for_non_existent_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book_ids = repo.get_book_ids_for_author('United States')

    assert len(book_ids) == 0


def test_repository_returns_date_of_previous_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book= repo.get_book(2250580)

    previous_date = repo.get_date_of_previous_book(book)

    assert previous_date == 2006



def test_repository_can_add_a_comment(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('thorke')
    book = repo.get_book(25742454)
    comment = make_comment("Trump's onto it!", user, book)

    repo.add_comment(comment)

    assert comment in repo.get_comments()

def test_repository_can_retrieve_comments(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert len(repo.get_comments()) == 5