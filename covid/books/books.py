from flask import Blueprint, render_template, url_for, request

from covid.books import services

import covid.adapters.repository as repo


books_blueprint = Blueprint('books_bp', __name__, url_prefix='/books')

@books_blueprint.route('/books_show', methods=['GET'])
def books_show():
    page_index=request.args.get('page')

    last_index=services.get_page_of_books(repo.repo_instance)

    first_book = services.get_first_book(repo.repo_instance)
    last_book = services.get_last_book(repo.repo_instance)

    if page_index is None:
        page_now=int(0)
    else:
        page_now=int(page_index)

    books, previous_date, next_date = services.get_number_books(page_now,3, last_index,repo.repo_instance)

    first_book_url = None
    last_book_url = None
    next_book_url = None
    prev_book_url = None

    if len(books) > 0:
        # There's at least one article for the target date.
         if previous_date is not None:
        # There are articles on a previous date, so generate URLs for the 'previous' and 'first' navigation buttons.
            first_book_url = url_for('books_bp.books_show', page=0)
            prev_book_url = url_for('books_bp.books_show', page=page_now-1)


            # There are articles on a subsequent date, so generate URLs for the 'next' and 'last' navigation buttons.
         if next_date is not None:
             next_book_url = url_for('books_bp.books_show', page=page_now+1)
             last_book_url = url_for('books_bp.books_show', page=last_index)



    return render_template('books/books.html',
                           selected_books=books,
                           first_book_url=first_book_url,
                           last_book_url=last_book_url,
                           prev_book_url=prev_book_url,
                           next_book_url=next_book_url
                           )
