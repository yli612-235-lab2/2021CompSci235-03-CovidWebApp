import csv
import json
from bisect import insort_left, bisect_left
from datetime import date, datetime
from pathlib import Path
from typing import List, Iterable, Any

from DateTime import DateTime
from werkzeug.security import generate_password_hash

from covid.adapters.repository import AbstractRepository
from covid.domain.model import User, Book, Author, Comment, make_author_association, make_comment, Publisher, \
    PopularShelve, make_popularshelve


class MemoryRepository(AbstractRepository):
    # Articles ordered by date, not id. id is assumed unique.
    def __init__(self):
        self.__books = list()
        self.__books_index = dict()
        self.__authors = list()
        self.__users = list()
        self.__comments = list()
        self.__popularshelves=list()
        self.__popularshelves_index= dict()

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

    def get_users(self) -> List[User]:
        return self.__users

    def get_number_of_user(self):
        return len(self.__users)

    def get_index_of_user(self,user):
        return self.__users.index(user)

    def add_book(self, book: Book):
        insort_left(self.__books, book)
        self.__books_index[book.book_id] = book

    def get_book(self, id: int) -> Book:
        book = None
        try:
            book = self.__books_index[id]
        except KeyError:
            pass  # Ignore exception and return None.
        return book

    # Helper method to return article index.
    def book_index(self, book: Book):
        index = bisect_left(self.__books, book)
        if index != len(self.__books) and self.__books[index].publication_year == book.publication_year:
            return index
        raise ValueError


    def get_books_by_publication_year(self, publication_year: int) -> List[Book]:
        matching_books = list()
        for book in self.__books:
            if book.publication_year == publication_year:
               matching_books.append(book)
        return matching_books

    def get_number_of_books(self):
        return len(self.__books)

    def get_first_book(self):
        book = None

        if len(self.__books) > 0:
            book = self.__books[0]
        return book

    def get_last_book(self):
        book = None
        if len(self.__books) > 0:
            book = self.__books[-1]
        return book

    def get_books_by_id(self, id_list):
        # Strip out any ids in id_list that don't represent Article ids in the repository.
        existing_ids = [id for id in id_list if id in self.__books_index]

        # Fetch the Articles.
        books = [self.__books_index[id] for id in existing_ids]
        return books

    def get_books_by_number(self, page_index:int,quantity:int):
        book_m=int(page_index)*int(quantity)
        books = list()
        index=int(0)

        for book in self.__books:
            if (index >= book_m) and (index<book_m+quantity):
                insort_left(books, book)
            index += 1
        return books


    def get_date_of_previous_book(self, book: Book):
        previous_date = None
        try:
            index = self.book_index(book)

            for stored_book in reversed(self.__books[0:index]):

                if int(stored_book.publication_year) < int(book.publication_year):
                    previous_date = stored_book.publication_year
                    break

        except ValueError:
            # No earlier articles, so return None.
            pass
        return previous_date

    def get_data_of_next_book(self, book: Book):
        next_date = None
        try:
            index = self.book_index(book)
            for stored_book in self.__books[index + 1:len(self.__books)]:
                if int(stored_book.publication_year) > int(book.publication_year):
                    next_date = stored_book.publication_year
                    break
        except ValueError:
            # No subsequent articles, so return None.
            pass

        return next_date

    def add_author(self, author: Author):
        self.__authors.append(author)

    def get_authors(self) -> List[Author]:
        return self.__authors

    def get_book_ids_for_author(self, author_name: str):
        # Linear search, to find the first occurrence of a Tag with the name tag_name.
        author = next((author for author in self.__authors if author.author_name == author_name), None)

        # Retrieve the ids of articles associated with the Tag.
        if author is not None:
            book_ids = [book.book_id for book in author.aurhor_books]
        else:
            # No Tag with name tag_name, so return an empty list.
            book_ids = list()
        return book_ids

    def add_comment(self, comment: Comment):
        # call parent class first, add_comment relies on implementation of code common to all derived classes
        super().add_comment(comment)
        self.__comments.append(comment)

    def get_comments(self):
        return self.__comments

    def get_number_of_comments(self):
        return len(self.__comments)

    def add_popularshelve(self,popularshelve:PopularShelve):
        popular_name=popularshelve.name
        if  popular_name  not in self.__popularshelves_index.keys():
            self.__popularshelves_index[popular_name] = list()
            self.__popularshelves.append(popularshelve)
        self.__popularshelves_index[popular_name].append(popularshelve.book_id)

    def get_popularshelves(self):
        return self.__popularshelves

    def get_number_of_popularshelves(self):
        return len(self.__popularshelves)

    def get_book_ids_for_popularshelve(self, target_date: str):
        # Linear search, to find the first occurrence of a Tag with the name tag_name.
        return self.__popularshelves_index[target_date]
#
#
#
#
# def write_csv_file(filename: str,row: Iterable):
#     with  open(filename,'a', newline='',encoding='utf-8-sig') as infile:
#          write=csv.writer(infile)
#          write.writerow(row)
#
#
#
# def read_csv_file(filename: str):
#     with open(filename, encoding='utf-8-sig') as infile:
#         reader = csv.reader(infile)
#         # Read first line of the the CSV file.
#         headers = next(reader)
#
#         # Read remaining rows from the CSV file.
#         for row in reader:
#             # Strip any leading/trailing white space from data read.
#             row = [item.strip() for item in row]
#             yield row
#
#
#
# def load_users(data_path: Path, repo: MemoryRepository):
#     users = dict()
#
#     users_filename = str(Path(data_path) / "users.csv")
#     for data_row in read_csv_file(users_filename):
#         user = User(
#             user_name=data_row[1],
#             password=generate_password_hash(data_row[2])
#         )
#         repo.add_user(user)
#         users[data_row[0]] = user
#     return users
#
#
# def load_books_and_authors(data_path: Path, repo: MemoryRepository):
#     authors_file_name = str(data_path / "book_authors_excerpt.json")
#     file_author = open(authors_file_name, 'r', encoding='utf-8')
#
#     author_list = dict()
#
#     for line in file_author.readlines():
#         author_dict = json.loads(line)
#         m_id = int(author_dict['author_id'])
#         m_name= author_dict['name']
#         if  m_id not in author_list.keys():
#             author_list[m_id]=m_name
#     # ===============================================================================
#     authors = dict()
#     books_file_name = str(data_path / "comic_books_excerpt.json")
#     file_book = open(books_file_name, 'r', encoding='utf-8')
#     for line in file_book.readlines():
#         load_dict = json.loads(line)
#
#         m_book_id=int(load_dict['book_id'])
#
#         m_publication_year=load_dict['publication_year']
#         m_publication_month = load_dict['publication_month']
#         m_publication_day = load_dict['publication_day']
#
#         if  m_publication_year=="":
#             m_publication_year =2021
#         else:
#             m_publication_year = int(m_publication_year)
#
#         if m_publication_month=="" or m_publication_day=="":
#             m_publication_month=1
#             m_publication_day=1
#
#         data=DateTime(int(m_publication_year),int(m_publication_month),int(m_publication_day))
#
#         m_publication_data=date.fromisoformat(data.strftime("%Y-%m-%d"))
#
#         m_publisher = load_dict['publisher']
#
#         publisher=Publisher(publisher_name=m_publisher,
#                             publication_data=m_publication_data
#                             )
#
#         m_book_authors=json.dumps(load_dict['authors'])
#
#         m_load_dict = json.loads(m_book_authors)
#
#         for author in m_load_dict:
#             author_id=int(author['author_id'])
#             if author_id not in authors.keys():
#                 authors[author_id] = list()
#             authors[author_id].append(m_book_id)
#
#         # print(m_publication_year)
#         # Create Book object.
#         book = Book(
#             publication_year=m_publication_year,
#             book_id=m_book_id,
#             title= load_dict['title'],
#             ebook= bool(load_dict['is_ebook']),
#             hyperlink=load_dict['url'],
#             image_hyperlink=load_dict['image_url'],
#             description=load_dict['description'],
#             publisher=publisher,
#             average_rating=load_dict['average_rating'],
#         )
#         # Add the Article to the repository.
#         repo.add_book(book)
#
#         m_popular_shelves=json.dumps(load_dict['popular_shelves'])
#
#         m_popular_dict = json.loads(m_popular_shelves)
#
#         for popular in m_popular_dict:
#             popular_count=int(popular['count'])
#             popular_name=popular['name']
#             popularshelve = PopularShelve(popular_count,popular_name)
#             make_popularshelve(book,popularshelve)
#             repo.add_popularshelve(m_book_id,popularshelve)
#
#
#     for author_id in authors.keys():
#         author_name=author_list[author_id]
#         author = Author(author_id,author_name)
#         for book_id in authors[author_id]:
#              book = repo.get_book(book_id)
#              make_author_association(book,author)
#         repo.add_author(author)
#
#     file_book.close()
#     file_author.close()
#
#
# def load_comments(data_path: Path, repo: MemoryRepository, users):
#     comments_filename = str(Path(data_path) / "comments.csv")
#     for data_row in read_csv_file(comments_filename):
#
#         comment = make_comment(
#             comment_text=data_row[3],
#             user=users[data_row[1]],
#             book=repo.get_book(int(data_row[2])),
#             timestamp=datetime.fromisoformat(data_row[4])
#         )
#
#         repo.add_comment(comment)
#
#
# def populate(data_path: Path, repo: MemoryRepository):
#
#     # Load articles and tags into the repository.
#     load_books_and_authors(data_path, repo)
#
#     # Load users into the repository.
#     users = load_users(data_path, repo)
#
#     # Load comments into the repository.
#     load_comments(data_path, repo, users)
#
#
