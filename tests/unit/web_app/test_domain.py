from covid.domain.model import Book, User, Author
import pytest

@pytest.fixture()
def book():
    return Book(
        2021,
        25742454,
        'The Switchblade Mamma',
        True,
        "https://www.goodreads.com/book/show/25742454-the-switchblade-mamma",
        "https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png",
        "Lillian Ann Cross is forced to live the worst nightmare of her life. She is an everyday middle class American,"
        '2021-01-01.',
        '4.12.'
    )


@pytest.fixture()
def user():
    return User('dbowie', '1234567890')


@pytest.fixture()
def author():
    return Author(2983296,'Anton Szandor LaVey')


def test_user_construction(user):
    assert user.user_name == 'dbowie'
    assert user.password == '1234567890'
    assert repr(user) == '<User dbowie 1234567890>'

    for comment in user.comments:
        # User should have an empty list of Comments after construction.
        assert False


def test_book_construction(book):
    assert book.book_id is None
    assert book.publication_year == 2021
    assert book.title == 'The Switchblade Mamma'
    assert book.ebook == True
    assert book.hyperlink == "https://www.goodreads.com/book/show/25742454-the-switchblade-mamma"
    assert book.image_hyperlink == "https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png"
    assert book.number_of_comments == 0
    assert book.number_of_authors == 0




def test_book_less_than_operator():
    book_1 = Book(
        '2020', None, None, None, None
    )

    book_2 = Book(
        '2021', None, None, None, None
    )

    assert book_1 < book_2