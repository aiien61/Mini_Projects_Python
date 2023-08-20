from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired
import requests

MOVIE_DB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
MOVIE_DB_API_KEY = "YOUR-API-KEY-FROM-TMDB"
MOVIE_DB_INFO_URL = "https://api.themoviedb.org/3/movie"
MOVIE_DB_IMG_URL = "https://image.tmdb.org/t/p/w500"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'GENERATE-YOUR-SECRET-KEY'
Bootstrap5(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movie-collection.db"
db = SQLAlchemy()
db.init_app(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f"<Movie {self.title}>"
    

class EditMovieForm(FlaskForm):
    rating = DecimalField('Your Rating Out of 10 e.g. 7.5',
                          validators=[DataRequired()])
    review = StringField('Your Review', validators=[DataRequired()])
    submit = SubmitField('Done')


class FindMovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    with app.app_context():
        result = db.session.execute(db.select(Movie).order_by(Movie.rating))
        all_movies = result.scalars().all()

        for i, movie in enumerate(all_movies[::-1], start=1):
            movie.ranking = i
    return render_template("index.html", all_movies=all_movies)


@app.route("/edit", methods=["GET", "POST"])
def edit_movie():
    form = EditMovieForm()
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data.strip()
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit.html', form=form, movie=movie)


@app.route("/delete")
def delete_movie():
    movie_to_delete = db.get_or_404(Movie, request.args.get("id"))
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = FindMovieForm()
    if form.validate_on_submit():
        parameters = {
            'api_key': MOVIE_DB_API_KEY,
            'query': form.title.data.strip()
        }
        response = requests.get(MOVIE_DB_SEARCH_URL, params=parameters)
        data = response.json()["results"]
        return render_template('select.html', options=data)
    return render_template('add.html', form=form)


@app.route("/find")
def find_movie():
    movie_id = request.args.get('id')
    if movie_id:
        movie_api_url = f"{MOVIE_DB_INFO_URL}/{movie_id}"
        parameters = {
            'api_key': MOVIE_DB_API_KEY,
            'language': "en-US"
        }
        response = requests.get(movie_api_url, params=parameters)
        data = response.json()
        new_movie = Movie(
            title=data["original_title"],
            year=int(data["release_date"].split('-')[0]),
            description=data["overview"],
            img_url=f"{MOVIE_DB_IMG_URL}{data['poster_path']}"
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('edit_movie', id=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)
