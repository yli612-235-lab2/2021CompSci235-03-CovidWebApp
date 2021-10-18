from flask import Blueprint, render_template, request, url_for

from covid.home import services
import covid.adapters.repository as repo

home_blueprint = Blueprint('home_bp', __name__)

@home_blueprint.route('/', methods=['GET'])
def home():

    popularshelves=services.get_popularshelve(repo.repo_instance)

    return render_template('home/home.html',
                           selectpopularshelves=popularshelves)


def get_aurthors_and_urls():
    author_names = services.get_author_names(repo.repo_instance)

    author_urls = dict()

    for author_name in author_names:
        author_urls[author_name] = url_for('news_bp.books_by_author', author=author_name)
    return author_urls


@home_blueprint.route('/books_by_popularshelve', methods=['GET'])
def books_by_popularshelve():
    target_date = request.args.get('data')
    # if  target_date is None:
    #     target_date="to-read"

    book_ids = services.get_book_ids_for_popularshelve(target_date, repo.repo_instance)

    books = services.get_books_by_id(book_ids, repo.repo_instance)

    return render_template('home/popularshelve.html',
                           selected_books=books,
                           author_urls=get_aurthors_and_urls())