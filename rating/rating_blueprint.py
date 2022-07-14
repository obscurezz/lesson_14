from flask import Blueprint, jsonify

from base_dao import BaseDao

rating_blueprint = Blueprint('rating_blueprint', __name__)

QUERY_CONSTRUCTOR = BaseDao(db='netflix.db')


@rating_blueprint.route('/rating/children')
def get_movies_children():
    movies_by_rating = QUERY_CONSTRUCTOR.get_titles_by_rating('G')
    return jsonify(movies_by_rating)


@rating_blueprint.route('/rating/family')
def get_movies_family():
    movies_by_rating = QUERY_CONSTRUCTOR.get_titles_by_rating('G', 'PG', 'PG-13')
    return jsonify(movies_by_rating)


@rating_blueprint.route('/rating/adult')
def get_movies_adult():
    movies_by_rating = QUERY_CONSTRUCTOR.get_titles_by_rating('R', 'NC-17')
    return jsonify(movies_by_rating)
