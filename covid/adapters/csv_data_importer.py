import csv

import json

from datetime import date, datetime

from collections import Iterable

from pathlib import Path

from DateTime import DateTime
from werkzeug.security import generate_password_hash

from covid.adapters.repository import AbstractRepository
from covid.domain.model import Publisher, Book, PopularShelve, make_popularshelve, make_author_association, Author, \
    User, make_comment


def write_csv_file(filename: str,row: Iterable):
    with  open(filename,'a', newline='',encoding='utf-8-sig') as infile:
         write=csv.writer(infile)
         write.writerow(row)

def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)
        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_books_and_authors(data_path: Path, repo: AbstractRepository, database_mode: bool):
    authors_file_name = str(data_path / "book_authors_excerpt.json")

    file_author = open(authors_file_name, 'r', encoding='utf-8')

    author_list = dict()

    for line in file_author.readlines():
        author_dict = json.loads(line)
        m_id = int(author_dict['author_id'])
        m_name= author_dict['name']
        if  m_id not in author_list.keys():
            author_list[m_id]=m_name

    # ===============================================================================
    authors = dict()
    books_file_name = str(data_path / "comic_books_excerpt.json")
    file_book = open(books_file_name, 'r', encoding='utf-8')
    for line in file_book.readlines():
        load_dict = json.loads(line)

        m_book_id=int(load_dict['book_id'])

        m_publication_year=load_dict['publication_year']
        m_publication_month = load_dict['publication_month']
        m_publication_day = load_dict['publication_day']

        if  m_publication_year=="":
            m_publication_year =2021
        else:
            m_publication_year = int(m_publication_year)

        if m_publication_month=="" or m_publication_day=="":
            m_publication_month=1
            m_publication_day=1

        data=DateTime(int(m_publication_year),int(m_publication_month),int(m_publication_day))

        m_publication_data=date.fromisoformat(data.strftime("%Y-%m-%d"))

        m_publisher = load_dict['publisher']

        # publisher=Publisher(publisher_name=m_publisher,
        #                     publication_data=m_publication_data)

        m_book_authors=json.dumps(load_dict['authors'])

        m_load_dict = json.loads(m_book_authors)

        for author in m_load_dict:
            author_id=int(author['author_id'])
            if author_id not in authors.keys():
                authors[author_id] = list()
            authors[author_id].append(m_book_id)

        m_title = load_dict['title']
        m_ebook = bool(load_dict['is_ebook'])
        m_hyperlink = load_dict['url']
        m_image_hyperlink = load_dict['image_url']
        m_description = load_dict['description']
        m_average_rating = load_dict['average_rating']

        # Create Book object.
        book = Book(
            publication_year=m_publication_year,
            publication_data=m_publication_data,
            book_id=m_book_id,
            title= m_title,
            ebook=m_ebook,
            hyperlink=m_hyperlink,
            image_hyperlink=m_image_hyperlink,
            description=m_description,
            publisher=m_publisher,
            average_rating=m_average_rating,
        )
        # Add the Article to the repository.
        repo.add_book(book)

        m_popular_shelves=json.dumps(load_dict['popular_shelves'])

        m_popular_dict = json.loads(m_popular_shelves)

        for popular in m_popular_dict:
            popular_count=int(popular['count'])
            popular_name=popular['name']
            popularshelve = PopularShelve(book, popular_count, popular_name)
            make_popularshelve(book,popularshelve)
            repo.add_popularshelve(popularshelve)


    for author_id in authors.keys():
        author_name=author_list[author_id]
        author = Author(author_id,author_name)
        for book_id in authors[author_id]:
             book = repo.get_book(book_id)
             make_author_association(book,author)

        repo.add_author(author)

    file_book.close()
    file_author.close()


def load_users(data_path: Path, repo: AbstractRepository):
    users = dict()
    users_filename = str(Path(data_path) / "users.csv")
    for data_row in read_csv_file(users_filename):
        user = User(
            user_name=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users

def load_comments(data_path: Path, repo: AbstractRepository, users):
    comments_filename = str(Path(data_path) / "comments.csv")

    for data_row in read_csv_file(comments_filename):

        comment = make_comment(
            comment_text=data_row[3],
            user=users[data_row[1]],
            book=repo.get_book(int(data_row[2])),
            timestamp=datetime.fromisoformat(data_row[4])
        )

        repo.add_comment(comment)


