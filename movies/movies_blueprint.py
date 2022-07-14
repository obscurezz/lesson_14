from flask import Blueprint, jsonify

from base_dao import BaseDao

movies_blueprint = Blueprint('movies_blueprint', __name__)

QUERY_CONSTRUCTOR = BaseDao(db='netflix.db')


@movies_blueprint.route('/movie/<title>')
def get_movie(title: str):
    movie_by_title = QUERY_CONSTRUCTOR.get_query_by_title(title)
    return movie_by_title


@movies_blueprint.route('/movie/<int:first>/to/<int:last>')
def get_movies_by_period(first: int, last: int):
    movies_by_period = QUERY_CONSTRUCTOR.get_titles_by_release_period(first, last)
    return jsonify(movies_by_period)
