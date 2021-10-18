from sqlalchemy import MetaData, Table, Column, String, Integer, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import mapper, relationship

from covid.domain import model

metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)


comments_table = Table(
    'comments', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('book_id', ForeignKey('books.book_id')),
    Column('comment', String(1024), nullable=False),
    Column('timestamp', DateTime, nullable=False)
)


books_table = Table(
    'books', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_id', Integer),
    Column('ebook', Boolean, nullable=False),
    Column('publication_year', Integer),
    Column('publication_data', String(255)),
    Column('title', String(255), nullable=False),
    Column('average_rating', String(255), nullable=False),
    Column('hyperlink', String(255), nullable=False),
    Column('image_hyperlink', String(255), nullable=False),
    Column('publisher', String(255)),
    Column('description', Text),
)

authors_table = Table(
    'authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('author_id', Integer),
    Column('author_name', String(64), nullable=False)
)

book_authors_table = Table(
    'book_authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_id', ForeignKey('books.book_id')),
    Column('author_id', ForeignKey('authors.author_id'))
)


popularshelves_table= Table(
    'popularshelves', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_id', ForeignKey('books.book_id')),
    Column('count', Integer),
    Column('name', String(64), nullable=False)
)




def map_model_to_tables():
    mapper(model.User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__comments': relationship(model.Comment, backref='_Comment__user')
    })

    mapper(model.Comment, comments_table, properties={
        '_Comment__comment': comments_table.c.comment,
        '_Comment__timestamp': comments_table.c.timestamp
    })
    mapper(model.PopularShelve, popularshelves_table, properties={
        '_PopularShelve__count': popularshelves_table.c.count,
        '_PopularShelve__name': popularshelves_table.c.name
    })
    mapper(model.Book, books_table, properties={
        '_Book__id': books_table.c.id,
        '_Book__book_id': books_table.c.book_id,
        '_Book__ebook': books_table.c.ebook,
        '_Book__title': books_table.c.title,
        '_Book__average_rating': books_table.c.average_rating,
        '_Book__hyperlink': books_table.c.hyperlink,
        '_Book__image_hyperlink': books_table.c.image_hyperlink,
        '_Book__publication_year': books_table.c.publication_year,
        '_Book__publication_data': books_table.c.publication_data,
        '_Book__publisher': books_table.c.publisher,
        '_Book__description': books_table.c.description,

        '_Book__comments': relationship(model.Comment, backref='_Comment__book'),
        '_Book__authors': relationship(model.Author, secondary=book_authors_table,
                                       back_populates='_Author__author_books'),
        '_Book__popularshelves': relationship(model.PopularShelve, backref='_PopularShelve__book'),
    })



    # '_Book__popularshelves': relationship(model.Comment, backref='_PopularShelve__book'),
    mapper(model.Author, authors_table, properties={
        '_Author__id': authors_table.c.id,
        '_Author__author_id': authors_table.c.author_id,
        '_Author__author_name': authors_table.c.author_name,
        '_Author__author_books':relationship(
            model.Book,
            secondary=book_authors_table,
            back_populates="_Book__authors"
        )
    })



