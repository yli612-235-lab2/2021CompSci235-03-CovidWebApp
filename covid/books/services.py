import random
from typing import Iterable

from covid.adapters.repository import AbstractRepository
from covid.domain.model import Book




class NonExistentArticleException(Exception):
    pass


class UnknownUserException(Exception):
    pass

def get_first_book(repo: AbstractRepository):

    book = repo.get_first_book()

    return book_to_dict(book)


def get_last_book(repo: AbstractRepository):
    book = repo.get_last_book()
    return book_to_dict(book)


def get_page_of_books(repo: AbstractRepository):
    book_count = repo.get_number_of_books()
    page_all=int(book_count/3)
    return page_all

def get_number_books(page_index,quantity,pages:int,repo: AbstractRepository):
    # Returns articles for the target date (empty if no matches), the date of the previous article (might be null), the date of the next article (might be null)
    book_count = repo.get_number_of_books()
    if quantity >= book_count:
        # Reduce the quantity of ids to generate if the repository has an insufficient number of articles.
        quantity = book_count - 1

    books = repo.get_books_by_number(page_index,quantity)

    books_dto = list()
    prev_date = next_date = None

    if len(books) > 0:
        if page_index==0:
            prev_date=None
            next_date = "next_date"
        elif page_index == pages:
            prev_date = "prev_date"
            next_date=None
        else:
            prev_date = "prev_date"
            next_date="next_date"

        # prev_date = repo.get_page_of_previous_book(page_index)
        # next_date = repo.get_page_of_next_book(page_index)

    # Convert Articles to dictionary form.
    books_dto = books_to_dict(books)

    return books_dto, prev_date, next_date


def book_to_dict(book: Book):
    article_dict = {

        'book_id': book.book_id,
        'description': book.description,
        'title': book.title,
        'hyperlink': book.hyperlink,
        'image_hyperlink': book.image_hyperlink,
    }
    return article_dict



def books_to_dict(books: Iterable[Book]):
    return [book_to_dict(book) for book in books]
