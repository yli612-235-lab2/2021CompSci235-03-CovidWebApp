import abc
from datetime import date
from typing import List
from covid.domain.model import User, Book, Author, Comment, PopularShelve

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        """ Returns the User named user_name from the repository.

        If there is no User with the given user_name, this method returns None.
        """
        raise NotImplementedError
    @abc.abstractmethod
    def get_users(self) -> List[User]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_user(self) -> int:

        raise NotImplementedError

    @abc.abstractmethod
    def add_book(self, book: Book):
        """ Adds an Article to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_book(self, id: int) -> Book:
        """ Returns Article with id from the repository.

        If there is no Article with the given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_by_publication_year(self, publication_year: int) -> List[Book]:
        """ Returns a list of Articles that were published on target_date.

        If there are no Articles on the given date, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_books(self) -> int:
        """ Returns the number of Articles in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_book(self) -> Book:
        """ Returns the first Article, ordered by date, from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_book(self) -> Book:
        """ Returns the last Article, ordered by date, from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_by_id(self, id_list):
        """ Returns a list of Articles, whose ids match those in id_list, from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError


    @abc.abstractmethod
    def get_books_by_number(self, page_index: int,quantity: int):

        raise NotImplementedError

    @abc.abstractmethod
    def get_date_of_previous_book(self, book: Book):
        """ Returns the date of an Article that immediately precedes article.

        If article is the first Article in the repository, this method returns None because there are no Articles
        on a previous date.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_data_of_next_book(self, book: Book):
        """ Returns the date of an Article that immediately follows article.

        If article is the last Article in the repository, this method returns None because there are no Articles
        on a later date.
        """
        raise NotImplementedError
    @abc.abstractmethod
    def add_author(self, author: Author):
        """ Adds a Tag to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_authors(self) -> List[Author]:
        """ Returns the Tags stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_ids_for_author(self, author_name: str):
        """ Returns a list of ids representing Articles that are tagged by tag_name.

        If there are Articles that are tagged by tag_name, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_comment(self, comment: Comment):
        """ Adds a Comment to the repository.

        If the Comment doesn't have bidirectional links with an Article and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if comment.user is None or comment not in comment.user.comments:
            raise RepositoryException('Comment not correctly attached to a User')
        if comment.book is None or comment not in comment.book.comments:
            raise RepositoryException('Comment not correctly attached to an Book')

    @abc.abstractmethod
    def get_comments(self):
        """ Returns the Comments stored in the repository. """
        raise NotImplementedError


    @abc.abstractmethod
    def get_number_of_comments(self) -> int:

        raise NotImplementedError

    def get_index_of_user(self, user):
        raise NotImplementedError

    def add_popularshelve(self,popularshelve: PopularShelve):
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_ids_for_popularshelve(self, target_date: str):
        """ Returns a list of ids representing Articles that are tagged by tag_name.

        If there are Articles that are tagged by tag_name, this method returns an empty list.
        """
        raise NotImplementedError