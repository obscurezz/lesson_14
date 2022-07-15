from flask import Blueprint, jsonify

from base_dao import BaseDao

genres_blueprint = Blueprint('genres_blueprint', __name__)

QUERY_CONSTRUCTOR = BaseDao(db='netflix.db')


@genres_blueprint.route('/genre/<genre>')
def get_movies_by_genre(genre: str):
    movies_by_genre = QUERY_CONSTRUCTOR.get_titles_by_genre(genre)
    if movies_by_genre is None:
        return jsonify({"error": "No such genres"}), 404
    else:
        return movies_by_genre, 200
