from datetime import datetime

import pytest

from covid.domain.model import User, make_comment, Comment

from covid.adapters.repository import RepositoryException


def test_repository_can_add_a_user(in_memory_repo):
    user = User('dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('dave') is user

def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '33vdfdgdgdfdfd')



def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('yyno')
    assert user is None

def test_repository_can_retrieve_book_count(in_memory_repo):
    number_of_books = in_memory_repo.get_number_of_books()

    # Check that the query returned 6 Articles.
    assert number_of_books == 20


def test_repository_does_not_retrieve_a_non_existent_book(in_memory_repo):
    book = in_memory_repo.get_book(1)
    assert book is None

def test_repository_can_get_first_book(in_memory_repo):
    book = in_memory_repo.get_first_book()
    assert book.title == 'Superman Archives, Vol. 2'


def test_repository_can_get_last_book(in_memory_repo):
    book = in_memory_repo.get_last_book()
    assert book.title == 'Bounty Hunter 4/3: My Life in Combat from Marine Scout Sniper to MARSOC'


def test_repository_can_get_books_by_ids(in_memory_repo):
    books = in_memory_repo.get_books_by_id([2250580, 27036538, 13571772])

    assert len(books) == 3
    assert books[
               0].title == 'A.I. Revolution, Vol. 1'
    assert books[1].title == "Crossed + One Hundred, Volume 2 (Crossed +100 #2)"
    assert books[2].title == 'Captain America: Winter Soldier (The Ultimate Graphic Novels Collection: Publication Order, #7)'

def test_repository_does_not_retrieve_book_for_non_existent_id(in_memory_repo):
    books = in_memory_repo.get_books_by_id([2250580, 9])

    assert len(books) == 1
    assert books[
               0].title == 'A.I. Revolution, Vol. 1'


def test_repository_returns_date_of_previous_book(in_memory_repo):
    book = in_memory_repo.get_book(13571772)
    previous_date = in_memory_repo.get_date_of_previous_book(book)

    assert previous_date == 2006

def test_repository_returns_none_when_there_are_no_previous_books(in_memory_repo):
    book = in_memory_repo.get_book(1)
    previous_date = in_memory_repo.get_date_of_previous_book(book)

    assert previous_date is None


def test_repository_can_add_a_comment(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    book = in_memory_repo.get_book(25742454)
    comment = make_comment("Trump's onto it!", user, book)

    in_memory_repo.add_comment(comment)

    assert comment in in_memory_repo.get_comments()

def test_repository_can_retrieve_comments(in_memory_repo):
    assert len(in_memory_repo.get_comments()) == 3






if __name__ == '__main__':
    pytest.main(["-s", "test_memory_repository.py"])