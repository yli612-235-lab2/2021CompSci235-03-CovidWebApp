from typing import List, Iterable
from datetime import date, datetime

class User:
    def __init__(self, user_name: str, password: str):
        self.__user_name: str = user_name
        self.__password: str = password
        self.__comments: List[Comment] = list()

    @property
    def user_name(self) -> str:
        return self.__user_name
    @property
    def password(self) -> str:
        return self.__password

    @property
    def comments(self) -> Iterable['Comment']:
        return iter(self.__comments)

    def add_comment(self, comment: 'Comment'):
        self.__comments.append(comment)

    def __repr__(self) -> str:
        return f'<User {self.__user_name} {self.__password}>'

    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return other.user_name == self.user_name

class Comment:
    def __init__(self, user: User, book: 'Book', comment: str, timestamp: datetime):
        self.__user: User = user
        self.__book: Book = book
        self.__comment: str = comment
        self.__timestamp: datetime = timestamp

    @property
    def user(self) -> User:
        return self.__user

    @property
    def book(self) -> 'Book':
        return self.__book

    @property
    def comment(self) -> str:
        return self.__comment

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    def __eq__(self, other):
        if not isinstance(other, Comment):
            return False
        return other.user == self.user and other.book == self.book and \
               other.comment == self.comment and other.timestamp == self.timestamp


    def __repr__(self):
        try:
            return f"<Comment  {self.comment}, book id = {self.book}>"
        except:
            raise ValueError



class PopularShelve:
     def __init__(self,book:'Book',count:int,name:str):
         self.__book=book
         self.__count=count;
         self.__name=name;

     @property
     def book(self) -> 'Book':
         return self.__book

     @property
     def name(self) -> str:
        return self.__name

     @property
     def cont(self) -> int:
        return self.__count

     def __repr__(self):
        # we use access via the property here
        return f'<Popular_Shelves {self.name}>'


class Publisher:
    def __init__(self, publisher_name: str,publication_data:str):
        self.__name = publisher_name;
        self.__publication_data = publication_data

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, publisher_name: str):
        self.__name = 'N/A'
        if isinstance(publisher_name, str):
            publisher_name = publisher_name.strip()
            if publisher_name != "":
                self.__name = publisher_name

    @property
    def publication_data(self):
        return self.__publication_data


    def __repr__(self):
        # we use access via the property here
        return f'<Publisher {self.name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other._name == self._name

    def __lt__(self, other):
        return self._name < other._name

    def __hash__(self):
        return hash(self._name)


class Book:
    def __init__(self,publication_year,publication_data,book_id,title,ebook,hyperlink,image_hyperlink,description,publisher,average_rating):
        if not isinstance(title, str) or len(title.strip()) == 0 or title == None:
            raise ValueError

        if type(book_id) != int or book_id < 0:
            raise ValueError

        if type(publication_year) != int or publication_year < 0:
            raise ValueError

        self.__book_id = book_id
        self.__ebook = ebook
        self.__publication_year = publication_year
        self.__publication_data = publication_data
        self.__title = title.strip()
        self.__average_rating=average_rating
        self.__hyperlink=hyperlink
        self.__image_hyperlink=image_hyperlink
        self.__publisher = publisher
        self.__description = description

        self.__authors: List[Author] = list()
        self.__comments: List[Comment] = list()
        self.__popularshelves:List[PopularShelve]=list()

    @property
    def book_id(self):
        return self.__book_id

    # gets the title
    @property
    def title(self):
        return self.__title

    # sets the title
    @title.setter
    def title(self, title):
        if not isinstance(title, str) or len(title.strip()) == 0 or title == None:
            raise ValueError
        else:
            self.__title = title.strip()

    @property
    def publisher(self):
        return self.__publisher

    @publisher.setter
    def publisher(self, publisher):
        self.__publisher = publisher

    @property
    def publication_year(self):
        return self.__publication_year

    @publication_year.setter
    def publication_year(self, publication_year):
        self.__publication_year = publication_year

    @property
    def publication_data(self):
        return self.__publication_data

    @property
    def average_rating(self):
        return self.__average_rating

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description: str):
        try:
            if not isinstance(description, str) or len(description) == 0:
                raise ValueError
        except ValueError:
            pass
        else:
            self.__description = description.strip()

    @property
    def ebook(self) -> int:
        return self.__ebook

    @ebook.setter
    def ebook(self, ebook: int):
        if type(ebook) != bool:
            raise ValueError
        else:
            self.__ebook = ebook

    @property
    def hyperlink(self) -> str:
        return self.__hyperlink

    @property
    def image_hyperlink(self) -> str:
        return self.__image_hyperlink

    @property
    def number_of_authors(self) -> int:
        return len(self.__authors)

    @property
    def authors(self) -> Iterable['Author']:
        return iter(self.__authors)

    def is_author_by(self, author: 'Author'):
        return author in self.__authors

    def is_author(self) -> bool:
        return len(self.__authors) > 0


    def add_author(self, author:'Author'):
        self.__authors.append(author)

    def remove_author(self, author:'Author'):
        if author in self.authors:
            self.__authors.remove(author)

    @property
    def comments(self) -> Iterable[Comment]:
        return iter(self.__comments)

    @property
    def number_of_comments(self) -> int:
        return len(self.__comments)

    def add_comment(self, comment: Comment):
        self.__comments.append(comment)

    @property
    def popularshelves(self) -> Iterable[PopularShelve]:
        return iter(self.__popularshelves)

    @property
    def number_of_popularshelves(self) -> int:
        return len(self.__popularshelves)

    def add_popularshelve(self, popularshelve: PopularShelve):
        self.__popularshelves.append(popularshelve)

    def is_applied_to(self, popularshelve: PopularShelve) -> bool:
        return popularshelve in self.__popularshelves


    def __repr__(self):
        try:
            return f"<Book {self.publication_year}, book id = {self.book_id}>"
        except:
            raise ValueError

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise ValueError
        return self.publication_year ==other.publication_year


    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise ValueError
        return self.publication_year < other.publication_year

    def __hash__(self):
        try:
            return hash(self.publication_year)
        except:
            raise ValueError

class Author:
    def __init__(self, author_id, author_full_name):
        if author_id < 0 or type(author_id) != int:
            raise ValueError("author_id")

        if type(author_full_name) != str or len(author_full_name.strip()) == 0:
            raise ValueError("author_full_name")

        self.__author_id = author_id
        self.__author_name = author_full_name
        self.__author_books: List[Book] = list()

        # self.coauthor_list = [self.unique_id]

    @property
    def author_name(self):
        return self.__author_name

    @author_name.setter
    def author_name(self, name):
        if type(name) == str and len(name.strip()) != 0:
            self.__author_name = name.strip()

    @property
    def author_id(self):
        return self.__author_id

    def __repr__(self):
        try:
            return f'<Author {self.author_name}, author id = {self.author_id}>'
        except:
            raise ValueError

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise ValueError
        return self.author_id == other.author_id

    def __lt__(self, other):
        try:
            return self.author_id < other.author_id
        except:
            raise ValueError

    def __hash__(self):
        try:
            return hash(self.author_id)
        except:
            raise ValueError

    @property
    def aurhor_books(self) -> Iterable[Book]:
        return iter(self.__author_books)

    @property
    def number_of_author_books(self) -> int:
        return len(self.__author_books)

    def is_applied_to(self, book: Book) -> bool:
        return book in self.__author_books

    def add_book(self, book: Book):
        self.__author_books.append(book)


class ModelException(Exception):
    pass

def make_comment(comment_text: str, user: User, book: Book, timestamp: datetime = datetime.today()):
    comment = Comment(user, book, comment_text, timestamp)
    user.add_comment(comment)
    book.add_comment(comment)
    return comment


def make_popularshelve(book:Book,popularshelve:PopularShelve):
    if book.is_applied_to(popularshelve)==False:
       book.add_popularshelve(popularshelve)




def make_author_association(book: Book,author: Author):
    if author.is_applied_to(book)==False:
       book.add_author(author)
       author.add_book(book)

