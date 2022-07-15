import sqlite3


def get_more_actors(actor_1: str, actor_2: str) -> list:
    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()
        # You can't use GROUP BY expression with HAVING COUNT() in this select below
        # because selected result is a string that contains every actor,
        # so you are just getting each group with count = 1
        query_result = cursor.execute(
                                     """
                                     SELECT "cast"
                                     FROM netflix
                                     WHERE "cast" LIKE :a1
                                     AND "cast" LIKE :a2
                                     """,
                                     {"a1": f'%{actor_1}%', "a2": f'%{actor_2}%'}
                                     )

        query_result = query_result.fetchall()
        query_result = [r[0].replace(f"{actor_1},", '').replace(f"{actor_2},", '').strip().split(', ') for r in
                        query_result]

    query_result = [row for row_s in query_result for row in row_s]
    function_result = list(set([actor for actor in query_result if query_result.count(actor) >= 2]))

    return function_result


def get_movie_by_params(form: str, year: int, genre: str) -> list[dict]:

    def dict_factory(curs, row):
        d = {}
        for idx, col in enumerate(curs.description):
            d[col[0]] = row[idx]
        return d

    with sqlite3.connect('netflix.db') as connection:
        connection.row_factory = dict_factory
        cursor = connection.cursor()

        query_result = cursor.execute(
                                     """
                                     SELECT title, description
                                     FROM netflix
                                     WHERE "type" = :form
                                     AND release_year = :year
                                     AND listed_in LIKE :genre
                                     ORDER BY release_year DESC
                                     """,
                                     {"form": form, "year": year, "genre": f'%{genre}%'}
                                     )

        query_result = query_result.fetchall()

    return query_result


print(get_more_actors('Rose McIver', 'Ben Lamb'))
print(get_more_actors('Jack Black', 'Dustin Hoffman'))

print(get_movie_by_params('Movie', 2007, 'Thriller'))
