import pytest
from flask import session


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid user name and password.
    response = client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost:4000/authentication/login'

@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
        ('fmercury', 'Test#6^0', b'Your user name is already taken - please supply another'),
))
def test_register_with_invalid_input(client, user_name, password, message):
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data

def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost:4000/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['user_name'] == 'thorke'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session

def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'The Browsing books of 2021' in response.data



def test_login_required_to_comment(client):
    response = client.post('/comment')
    assert response.headers['Location'] == 'http://localhost:4000/authentication/login'

def test_comment(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the comment page.
    response = client.get('/comment?book=13571772')

    response = client.post(
        '/comment',
        data={'comment': 'Who needs quarantine?', 'book_id': 13571772}
    )
    assert response.headers['Location'] == 'http://localhost:4000/books_by_date?date=2021&view_comments_for=13571772'


@pytest.mark.parametrize(('comment', 'messages'), (
        ('Who thinks Trump is a f***wit?', (b'Your comment must not contain profanity')),
        ('Hey', (b'Your comment is too short')),
        ('ass', (b'Your comment is too short', b'Your comment must not contain profanity')),
))
def test_comment_with_invalid_input(client, auth, comment, messages):
    # Login a user.
    auth.login()

    # Attempt to comment on an article.
    response = client.post(
        '/comment',
        data={'comment': comment, 'book_id': 13571772}
    )
    # Check that supplying invalid comment text generates appropriate error messages.
    for message in messages:
        assert message in response.data


def test_books_without_date(client):
    # Check that we can retrieve the articles page.
    response = client.get('/books_by_date')
    assert response.status_code == 200

    assert b'Friday February 28 2020' in response.data
    assert b'Coronavirus: First case of virus in New Zealand' in response.data


def test_books_with_date(client):
    # Check that we can retrieve the articles page.
    response = client.get('/articles_by_date?date=2006')
    assert response.status_code == 200

    # Check that all articles on the requested date are included on the page.
    assert b'The Thing: Idol of Millions' in response.data



def test_articles_with_comment(client):
    # Check that we can retrieve the articles page.
    response = client.get('/books_by_date?date=2021&view_comments_for=13571772')
    assert response.status_code == 200

    # Check that all comments for specified article are included on the page.
    assert b'test my comment' in response.data



if __name__ == '__main__':
    pytest.main(["-s", "test_web_app.py"])  # 调用pytest的main函数执行测试

