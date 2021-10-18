from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from covid.adapters.repository import AbstractRepository
from covid.domain.model import User, Book, Comment, Author, PopularShelve


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def get_users(self) -> List[User]:
        users = self._session_cm.session.query(User).all()
        return users


    def get_number_of_user(self):
        number_of_users = self._session_cm.session.query(User).count()
        return number_of_users


    def add_book(self, book: Book):
        with self._session_cm as scm:
            scm.session.add(book)
            scm.commit()

    def get_book(self, id: int) -> Book:
        book = None
        try:
            book = self._session_cm.session.query(Book).filter(Book._Book__book_id == id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return book

    def get_books_by_publication_year(self, publication_year: int) -> List[Book]:
        if publication_year is None:
            books = self._session_cm.session.query(Book).all()
            return books
        else:
            # Return articles matching target_date; return an empty list if there are no matches.
            books = self._session_cm.session.query(Book).filter(Book._Book__publication_year == publication_year).all()
            return books

    def get_number_of_books(self):
        number_of_books = self._session_cm.session.query(Book).count()
        return number_of_books

    def get_first_book(self):
        book = self._session_cm.session.query(Book).first()
        return book

    def get_last_book(self):
        book = self._session_cm.session.query(Book).order_by(desc(Book._Book__book_id)).first()
        return book

    def get_books_by_id(self, id_list: List[int]):
        books = self._session_cm.session.query(Book).filter(Book._Book__book_id.in_(id_list)).all()
        return books

    def get_books_by_number(self, page_index: int, quantity: int):
        book_m = int(page_index) * int(quantity)
        books =self._session_cm.session.query(Book).limit(quantity).offset(book_m).all()
        return books

    def get_date_of_previous_book(self, book: Book):
        result = None
        prev_book = self._session_cm.session.query(Book).filter(Book._Book__publication_year < book.publication_year).order_by(desc(Book._Book__publication_year)).first()

        if prev_book is not None:
            result = prev_book.publication_year

        return result

    def get_data_of_next_book(self, book: Book):
        result = None
        next_book = self._session_cm.session.query(Book).filter(Book._Book__publication_year > book.publication_year).order_by(asc(Book._Book__publication_year)).first()

        if next_book is not None:
            result = next_book.publication_year

        return result

    def add_author(self, author: Author):
        with self._session_cm as scm:
            scm.session.add(author)
            scm.commit()

    def get_authors(self) -> List[Author]:
        authors = self._session_cm.session.query(Author).all()
        return authors

    def get_book_ids_for_author(self, author_name: str):
        book_ids = []

        # Use native SQL to retrieve article ids, since there is no mapped class for the article_tags table.
        row = self._session_cm.session.execute('SELECT author_id FROM authors WHERE author_name = :author_name', {'author_name': author_name}).fetchone()

        if row is None:
            # No tag with the name tag_name - create an empty list.
            book_ids = list()
        else:
            author_id = row[0]
            # Retrieve article ids of articles associated with the tag.
            book_ids = self._session_cm.session.execute(
                    'SELECT book_id FROM book_authors WHERE author_id = :author_id ORDER BY book_id ASC',
                    {'author_id': author_id}
            ).fetchall()


            book_ids = [id[0] for id in book_ids]

        return book_ids

    def add_comment(self, comment: Comment):
        super().add_comment(comment)

        with self._session_cm as scm:
            scm.session.add(comment)
            scm.commit()

    def get_comments(self) -> List[Comment]:
        comments = self._session_cm.session.query(Comment).all()
        return comments


    def get_number_of_comments(self):
        number_of_comments = self._session_cm.session.query(Comment).count()
        return number_of_comments

    def add_popularshelve(self,popularshelve: PopularShelve):
        # super().add_popularshelve(popularshelve)
        with self._session_cm as scm:
            scm.session.add(popularshelve)
            scm.commit()

    def get_popularshelves(self):
        popularshelves = self._session_cm.session.query(PopularShelve).all()
        return popularshelves

    def get_number_of_popularshelves(self):
        number_of_popularshelves = self._session_cm.session.query(PopularShelve).count()
        return number_of_popularshelves

    def get_book_ids_for_popularshelve(self, target_date: str):

        book_ids = []

        # Use native SQL to retrieve article ids, since there is no mapped class for the article_tags table.
        book_ids = self._session_cm.session.execute('SELECT book_id FROM popularshelves WHERE name = :popularShelve_name',
                                               {'popularShelve_name': target_date}).fetchall()

        book_ids = [id[0] for id in book_ids]

        return book_ids

