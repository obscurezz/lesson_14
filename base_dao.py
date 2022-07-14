import sqlite3

query_to_json = lambda columns, tup: dict(zip(columns, tup))


class BaseDao:
    def __init__(self, db: str):
        self.db = db

    def get_query_by_title(self, title_val: str) -> dict | str:
        """
        :param title_val: name of the movie
        :return: dict with exact columns for this movie in database
        """
        err = 'No such title in the database'
        columns = ('title', 'country', 'release_year', 'genre', 'description')

        with sqlite3.connect(self.db) as connection:
            cursor = connection.cursor()

            sql_query = f"SELECT title, country, release_year, listed_in, description FROM netflix WHERE title = '{title_val}' ORDER BY release_year DESC LIMIT 1"
            result = cursor.execute(sql_query)

            selected_table = result.fetchone()
        if selected_table is None:
            return err
        return query_to_json(columns, selected_table)

    def get_titles_by_release_period(self, first_year: int, last_year: int) -> list[dict] | str:
        """
        :param first_year: year from which we start finding
        :param last_year: year to which we stop finding
        :return: top 100 results between first year and last year
        """
        err = 'No movies in this period'
        columns = ('title', 'release_year')

        with sqlite3.connect(self.db) as connection:
            cursor = connection.cursor()

            sql_query = f"SELECT title, release_year FROM netflix WHERE release_year BETWEEN {first_year} AND {last_year} LIMIT 100"
            result = cursor.execute(sql_query)

            selected_table = result.fetchall()

        json_result = []
        for row in selected_table:
            json_result.append(query_to_json(columns, row))

        if len(json_result) == 0:
            return err
        return json_result

    def get_titles_by_rating(self, *ratings: str) -> list[dict]:
        """
        :param ratings: PG ratings for films we want to find
        :return: result json by the ratings were given
        """
        columns = ('title', 'rating', 'description')

        with sqlite3.connect(self.db) as connection:
            cursor = connection.cursor()

            if len(ratings) == 1:
                # if there is only 1 rating given we just give exact expression
                sql_query = f"SELECT title, rating, description FROM netflix WHERE rating = '{ratings[0]}' ORDER BY rating"
            else:
                # if there are few ratings given we use IN operator to find all of them
                sql_query = f"SELECT title, rating, description FROM netflix WHERE rating IN {ratings} ORDER BY rating"
            result = cursor.execute(sql_query)

            selected_table = result.fetchall()

        json_result = []
        for row in selected_table:
            json_result.append(query_to_json(columns, row))

        return json_result

    def get_titles_by_genre(self, genre: str) -> list[dict] | str:
        """
        :param genre: genre of movie we are searching
        :return: result json with 10 latest movies of current genre
        """
        err = 'No such genre in the database'
        columns = ('title', 'description')

        with sqlite3.connect(self.db) as connection:
            cursor = connection.cursor()

            sql_query = f"SELECT title, description FROM netflix WHERE listed_in LIKE '%{genre}%' ORDER BY release_year DESC LIMIT 10"
            result = cursor.execute(sql_query)

            selected_table = result.fetchall()

        json_result = []
        for row in selected_table:
            json_result.append(query_to_json(columns, row))

        if len(json_result) == 0:
            return err
        return json_result