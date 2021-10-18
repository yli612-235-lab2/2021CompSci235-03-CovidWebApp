from pathlib import Path
from typing import Iterable

from covid.adapters.csv_data_importer import write_csv_file
from covid.adapters.repository import AbstractRepository
from covid.domain.model import Author, Book, Comment, make_comment

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

def get_book(book_id: int, repo: AbstractRepository):
    book = repo.get_book(book_id)

    if book is None:
        raise NonExistentArticleException

    return book_to_dict(book)


def get_books_by_date(date, repo: AbstractRepository):
    # Returns articles for the target date (empty if no matches), the date of the previous article (might be null), the date of the next article (might be null)
    books = repo.get_books_by_publication_year(publication_year=date)
    books_dto = list()

    prev_date = next_date = None

    if len(books) > 0:
        prev_date = repo.get_date_of_previous_book(books[0])
        next_date = repo.get_data_of_next_book(books[0])
        # Convert Articles to dictionary form.

    books_dto = books_to_dict(books)

    return books_dto, prev_date, next_date


def get_book_ids_for_author(author_name, repo: AbstractRepository):
    book_ids = repo.get_book_ids_for_author(author_name)

    return book_ids

def get_books_by_id(id_list,quantity,repo: AbstractRepository):

    books = repo.get_books_by_id(id_list)




    # Convert Articles to dictionary form.
    books_as_dict = books_to_dict(books)

    return books_as_dict

def get_book(book_id: int, repo: AbstractRepository):
    book = repo.get_book(book_id)

    if book is None:
        raise NonExistentArticleException

    return book_to_dict(book)

def get_author_names(repo: AbstractRepository):
    authors = repo.get_authors()
    author_names = [author.author_name for author in authors]

    return author_names


def write_comment(book_id: int,comment_text: str,comment,user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException
    my_comment=[]
    my_comment.append(repo.get_number_of_comments())
    my_comment.append(repo.get_index_of_user(user))
    my_comment.append(book_id)

    my_comment.append(comment_text)
    my_comment.append(comment.timestamp)

    data_path = Path('MyWeb') / 'adapters' / 'data'

    comments_filename = str(Path(data_path) / "comments.csv")

    write_csv_file(comments_filename,my_comment)

#
# def sql_write_comment(book_id: int, comment_text: str, comment, user_name: str, repo: AbstractRepository):
#     user = repo.get_user(user_name)
#     if user is None:
#         raise UnknownUserException
#     add_sql_comments(repo.get_number_of_comments(),repo.get_index_of_user(user),book_id,comment_text,comment.timestamp)
#


def add_comment(book_id: int, comment_text: str, user_name: str, repo: AbstractRepository):
    # Check that the article exists.
    book = repo.get_book(book_id)
    if book is None:
        raise NonExistentArticleException

    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    # Create comment.
    comment = make_comment(comment_text, user, book)

    # Update the repository.
    repo.add_comment(comment)
    return comment


def get_comments_for_book(book_id, repo: AbstractRepository):
    book = repo.get_book(book_id)

    if book is None:
        raise NonExistentArticleException

    return comments_to_dict(book.comments)


def book_to_dict(book: Book):
    book_dict = {
        'publication_year': book.publication_year,
        'book_id': book.book_id,
        'description': book.description,
        'publisher': book.publisher,
        'publication_data': book.publication_data,
        'average_rating':book.average_rating,
        'title': book.title,
        'hyperlink': book.hyperlink,
        'image_hyperlink': book.image_hyperlink,
        'comments': comments_to_dict(book.comments),
        'authors': authors_to_dict(book.authors)
    }
    return book_dict


def books_to_dict(books: Iterable[Book]):
    return [book_to_dict(book) for book in books]


def author_to_dict(author: Author):
    author_dict = {
        'id': author.author_id,
        'name': author.author_name,
        'author_books': [book.book_id for book in author.aurhor_books]
    }
    return author_dict


def authors_to_dict(authors: Iterable[Author]):
    return [author_to_dict(author) for author in authors]


def comment_to_dict(comment: Comment):
    comment_dict = {
        'user_name': comment.user.user_name,
        'book_id': comment.book.book_id,
        'comment_text': comment.comment,
        'timestamp': comment.timestamp
    }
    return comment_dict


def comments_to_dict(comments: Iterable[Comment]):
    return [comment_to_dict(comment) for comment in comments]




