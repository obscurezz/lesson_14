from flask import Blueprint, jsonify

from base_dao import BaseDao

genres_blueprint = Blueprint('genres_blueprint', __name__)

QUERY_CONSTRUCTOR = BaseDao(db='netflix.db')


@genres_blueprint.route('/genre/<genre>')
def get_movies_by_genre(genre: str):
    movies_by_genre = QUERY_CONSTRUCTOR.get_titles_by_genre(genre)
    return jsonify(movies_by_genre)
