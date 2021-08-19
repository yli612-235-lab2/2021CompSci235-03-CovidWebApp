import csv
from pathlib import Path
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from covid.adapters.repository import AbstractRepository, RepositoryException
from covid.domain.model import Article, Tag, User, Comment, make_tag_association, make_comment


class MemoryRepository(AbstractRepository):
    # Articles ordered by date, not id. id is assumed unique.

    def __init__(self):
        self.__articles = list()
        self.__articles_index = dict()
        self.__tags = list()
        self.__users = list()
        self.__comments = list()

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

    def add_article(self, article: Article):
        insort_left(self.__articles, article)
        self.__articles_index[article.id] = article

    def get_article(self, id: int) -> Article:
        article = None

        try:
            article = self.__articles_index[id]
        except KeyError:
            pass  # Ignore exception and return None.

        return article

    def get_articles_by_date(self, target_date: date) -> List[Article]:
        target_article = Article(
            date=target_date,
            title=None,
            first_paragraph=None,
            hyperlink=None,
            image_hyperlink=None
        )
        matching_articles = list()

        try:
            index = self.article_index(target_article)
            for article in self.__articles[index:None]:
                if article.date == target_date:
                    matching_articles.append(article)
                else:
                    break
        except ValueError:
            # No articles for specified date. Simply return an empty list.
            pass

        return matching_articles

    def get_number_of_articles(self):
        return len(self.__articles)

    def get_first_article(self):
        article = None

        if len(self.__articles) > 0:
            article = self.__articles[0]
        return article

    def get_last_article(self):
        article = None

        if len(self.__articles) > 0:
            article = self.__articles[-1]
        return article

    def get_articles_by_id(self, id_list):
        # Strip out any ids in id_list that don't represent Article ids in the repository.
        existing_ids = [id for id in id_list if id in self.__articles_index]

        # Fetch the Articles.
        articles = [self.__articles_index[id] for id in existing_ids]
        return articles

    def get_article_ids_for_tag(self, tag_name: str):
        # Linear search, to find the first occurrence of a Tag with the name tag_name.
        tag = next((tag for tag in self.__tags if tag.tag_name == tag_name), None)

        # Retrieve the ids of articles associated with the Tag.
        if tag is not None:
            article_ids = [article.id for article in tag.tagged_articles]
        else:
            # No Tag with name tag_name, so return an empty list.
            article_ids = list()

        return article_ids

    def get_date_of_previous_article(self, article: Article):
        previous_date = None

        try:
            index = self.article_index(article)
            for stored_article in reversed(self.__articles[0:index]):
                if stored_article.date < article.date:
                    previous_date = stored_article.date
                    break
        except ValueError:
            # No earlier articles, so return None.
            pass

        return previous_date

    def get_date_of_next_article(self, article: Article):
        next_date = None

        try:
            index = self.article_index(article)
            for stored_article in self.__articles[index + 1:len(self.__articles)]:
                if stored_article.date > article.date:
                    next_date = stored_article.date
                    break
        except ValueError:
            # No subsequent articles, so return None.
            pass

        return next_date

    def add_tag(self, tag: Tag):
        self.__tags.append(tag)

    def get_tags(self) -> List[Tag]:
        return self.__tags

    def add_comment(self, comment: Comment):
        # call parent class first, add_comment relies on implementation of code common to all derived classes
        super().add_comment(comment)
        self.__comments.append(comment)

    def get_comments(self):
        return self.__comments

    # Helper method to return article index.
    def article_index(self, article: Article):
        index = bisect_left(self.__articles, article)
        if index != len(self.__articles) and self.__articles[index].date == article.date:
            return index
        raise ValueError


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


def load_articles_and_tags(data_path: Path, repo: MemoryRepository):
    tags = dict()

    articles_filename = str(data_path / "news_articles.csv")
    for data_row in read_csv_file(articles_filename):

        article_key = int(data_row[0])
        number_of_tags = len(data_row) - 6
        article_tags = data_row[-number_of_tags:]

        # Add any new tags; associate the current article with tags.
        for tag in article_tags:
            if tag not in tags.keys():
                tags[tag] = list()
            tags[tag].append(article_key)
        del data_row[-number_of_tags:]

        # Create Article object.
        article = Article(
            date=date.fromisoformat(data_row[1]),
            title=data_row[2],
            first_paragraph=data_row[3],
            hyperlink=data_row[4],
            image_hyperlink=data_row[5],
            id=article_key
        )

        # Add the Article to the repository.
        repo.add_article(article)

    # Create Tag objects, associate them with Articles and add them to the repository.
    for tag_name in tags.keys():
        tag = Tag(tag_name)
        for article_id in tags[tag_name]:
            article = repo.get_article(article_id)
            make_tag_association(article, tag)
        repo.add_tag(tag)


def load_users(data_path: Path, repo: MemoryRepository):
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


def load_comments(data_path: Path, repo: MemoryRepository, users):
    comments_filename = str(Path(data_path) / "comments.csv")
    for data_row in read_csv_file(comments_filename):
        comment = make_comment(
            comment_text=data_row[3],
            user=users[data_row[1]],
            article=repo.get_article(int(data_row[2])),
            timestamp=datetime.fromisoformat(data_row[4])
        )
        repo.add_comment(comment)


def populate(data_path: Path, repo: MemoryRepository):
    # Load articles and tags into the repository.
    load_articles_and_tags(data_path, repo)

    # Load users into the repository.
    users = load_users(data_path, repo)

    # Load comments into the repository.
    load_comments(data_path, repo, users)
