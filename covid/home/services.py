from typing import Iterable

from covid.adapters.repository import AbstractRepository
from covid.domain.model import PopularShelve, Book, Author, Comment


def get_popularshelve(repo: AbstractRepository):
    popularshelves = repo.get_popularshelves()

    popularshelvess_dto=popularshelves_to_dict(popularshelves)
    return popularshelvess_dto


def get_book_ids_for_popularshelve(target_date, repo: AbstractRepository):
    book_ids = repo.get_book_ids_for_popularshelve(target_date)

    return book_ids


def get_books_by_id(id_list,repo: AbstractRepository):
    count=len(id_list)
    books = repo.get_books_by_id(id_list)
    # # Convert Articles to dictionary form.
    books_as_dict = books_to_dict(books)

    return books_as_dict


def get_author_names(repo: AbstractRepository):
    authors = repo.get_authors()
    author_names = [author.full_name for author in authors]

    return author_names


def book_to_dict(book: Book):
    book_dict = {
        'publication_year': book.publication_year,
        'book_id': book.book_id,
        'description': book.description,
        'publisher': book.publisher.name,
        'publication_data': book.publisher.publication_data,
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
        'id': author.unique_id,
        'name': author.full_name,
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



def popularshelve_to_dict(popularshelve:PopularShelve):
    popularshelve_dict = {
        'name': popularshelve.name,
    }
    return popularshelve_dict



def popularshelves_to_dict(popularshelves: Iterable[PopularShelve]):
    return [popularshelve_to_dict(popularshelve) for popularshelve in popularshelves]