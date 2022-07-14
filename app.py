from flask import Flask
from movies import movies_blueprint
from rating import rating_blueprint
from genres import genres_blueprint


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False

app.register_blueprint(movies_blueprint)
app.register_blueprint(rating_blueprint)
app.register_blueprint(genres_blueprint)

app.run(port=8080, debug=True)
