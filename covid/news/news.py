# Configure Blueprint.
from datetime import date

from better_profanity import profanity
from flask import Blueprint, render_template, url_for, request, session,redirect
from flask_wtf import FlaskForm

from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import covid.adapters.repository as repo
from covid.authentication.authentication import login_required
from covid.news import services

news_blueprint = Blueprint(
    'news_bp', __name__)

@news_blueprint.route('/books_by_date', methods=['GET'])
def books_by_date():
    target_date = request.args.get('date')
    book_to_show_comments = request.args.get('view_comments_for')

    first_book = services.get_first_book(repo.repo_instance)
    last_book = services.get_last_book(repo.repo_instance)

    if target_date is None:
        target_date=2021

    if book_to_show_comments is None:
        # No view-comments query parameter, so set to a non-existent article id.
        book_to_show_comments = -1
    else:
        # Convert article_to_show_comments from string to int.
        book_to_show_comments = int(book_to_show_comments)

    books, previous_date, next_date = services.get_books_by_date(int(target_date), repo.repo_instance)
    # print(books)
    # print(previous_date, next_date)

    first_book_url = None
    last_book_url = None
    next_book_url = None
    prev_book_url = None


    if len(books) > 0:
        # There's at least one article for the target date.
        if previous_date is not None:
            # There are articles on a previous date, so generate URLs for the 'previous' and 'first' navigation buttons.
           prev_book_url = url_for('news_bp.books_by_date', date=previous_date)
           first_book_url = url_for('news_bp.books_by_date', date=first_book['publication_year'])

        # There are articles on a subsequent date, so generate URLs for the 'next' and 'last' navigation buttons.
        if next_date is not None:
            next_book_url = url_for('news_bp.books_by_date', date=next_date)
            last_book_url = url_for('news_bp.books_by_date', date=last_book['publication_year'])
        # Construct urls for viewing article comments and adding comments.
        for book in books:
            book['view_comment_url'] = url_for('news_bp.books_by_date', date=target_date, view_comments_for=book['book_id'])
            book['add_comment_url'] = url_for('news_bp.comment_on_book', book=book['book_id'])


    return render_template(
        'news/books.html',
        books_title='Book publication year : ' + str(target_date),
        selected_books=books,
        author_urls=get_aurthors_and_urls(),
        first_book_url=first_book_url,
        last_book_url=last_book_url,
        prev_book_url=prev_book_url,
        next_book_url=next_book_url,
        show_comments_for_book=book_to_show_comments
    )

    return redirect(url_for('home_bp.home'))


@news_blueprint.route('/comment', methods=['GET', 'POST'])
@login_required
def comment_on_book():
    # Obtain the user name of the currently logged in user.
    user_name = session['user_name']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an article id, when subsequently called with a HTTP POST request, the article id remains in the
    # form.
    form = CommentForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the comment text has passed data validation.
        # Extract the article id, representing the commented article, from the form.
        book_id = int(form.book_id.data)

        # Use the service layer to store the new comment.
        comment=services.add_comment(book_id, form.comment.data, user_name, repo.repo_instance)

        #services.write_comment(book_id,form.comment.data,comment, user_name, repo.repo_instance)

        # Retrieve the article in dict form.
        book = services.get_book(book_id, repo.repo_instance)

        # Cause the web browser to display the page of all articles that have the same date as the commented article,
        # and display all comments, including the new comment.
        return redirect(url_for('news_bp.books_by_date', date=book['publication_year'], view_comments_for=book_id))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the article id, representing the article to comment, from a query parameter of the GET request.
        book_id = int(request.args.get('book'))

        # Store the article id in the form.
        form.book_id.data = book_id
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the article id of the article being commented from the form.
        book_id = int(form.book_id.data)

    # For a GET or an unsuccessful POST, retrieve the article to comment in dict form, and return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.
    book = services.get_book(book_id, repo.repo_instance)

    return render_template(
        'news/comment_on_book.html',
        title='Edit book',
        book=book,
        form=form,
        handler_url=url_for('news_bp.comment_on_book'),
        author_urls=get_aurthors_and_urls()
    )

def get_selected_books(quantity=3):
    books = services.get_random_books(quantity, repo.repo_instance)
    for book in books:
        book['hyperlink'] = url_for('news_bp.articles_by_date', date=book['date'])

    return books



def get_aurthors_and_urls():
    author_names = services.get_author_names(repo.repo_instance)

    author_urls = dict()

    for author_name in author_names:
        author_urls[author_name] = url_for('news_bp.books_by_author', author=author_name)
    return author_urls

class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)

class CommentForm(FlaskForm):
    comment = TextAreaField(' My  Comment', [
        DataRequired(),
        Length(min=4, message='Your comment is too short'),
        ProfanityFree(message='Your comment must not contain profanity')])
    book_id = HiddenField("book id")
    submit = SubmitField('Submit')


#    ================================================================================
#    ================================================================================
@news_blueprint.route('/books_by_author', methods=['GET'])
def books_by_author():
    books_per_page = 3

    author_name = request.args.get('author')

    if author_name is None:
       author_name="Naoki Urasawa"

    cursor = request.args.get('cursor')

    book_to_show_comments = request.args.get('view_comments_for')

    if book_to_show_comments is None:
        # No view-comments query parameter, so set to a non-existent article id.
        book_to_show_comments = -1
    else:
        # Convert article_to_show_comments from string to int.
        book_to_show_comments = int(book_to_show_comments)

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    book_ids = services.get_book_ids_for_author(author_name, repo.repo_instance)

    books = services.get_books_by_id(book_ids,books_per_page, repo.repo_instance)

    first_book_url = None
    last_book_url = None
    next_book_url = None
    prev_book_url = None

    if cursor > 0:
        # There are preceding articles, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_book_url = url_for('news_bp.books_by_author', author=author_name, cursor=cursor - books_per_page)
        first_book_url = url_for('news_bp.books_by_author', author=author_name)

    if cursor + books_per_page < len(book_ids):
        # There are further articles, so generate URLs for the 'next' and 'last' navigation buttons.
        next_book_url = url_for('news_bp.books_by_author', author=author_name, cursor=cursor + books_per_page)

        last_cursor = books_per_page * int(len(book_ids) / books_per_page)
        if len(book_ids) % books_per_page == 0:
            last_cursor -= books_per_page

        last_book_url = url_for('news_bp.books_by_author', author=author_name, cursor=last_cursor)

        # Construct urls for viewing article comments and adding comments.
    for book in books:
        book['view_comment_url'] = url_for('news_bp.books_by_author', author=author_name, cursor=cursor,
                                              view_comments_for=book['book_id'])
        book['add_comment_url'] = url_for('news_bp.comment_on_book', book=book['book_id'])

    # Generate the webpage to display the articles.
    return render_template(
        'news/books.html',
        books_title='Books  by ' + author_name,
        selected_books=books,
        author_urls=get_aurthors_and_urls(),
        first_book_url=first_book_url,
        last_book_url=last_book_url,
        prev_book_url=prev_book_url,
        next_book_url=next_book_url,
        show_comments_for_book=book_to_show_comments
    )