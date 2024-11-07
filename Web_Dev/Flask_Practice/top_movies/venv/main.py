from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, HiddenField
from wtforms.validators import DataRequired
import requests

'''
On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt
'''

API_KEY: str = "YOUR API KEY"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'something-secret'
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db_name: str = "movies.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_name}"
db.init_app(app)

# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

with app.app_context():
    db.create_all()

# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
# second_movie = Movie(
#     title="Avatar The Way of Water",
#     year=2022,
#     description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
#     rating=7.3,
#     ranking=9,
#     review="I liked the water.",
#     img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
# )
# with app.app_context():
#     db.session.add(new_movie)
#     db.session.add(second_movie)
#     db.session.commit()


class RateMovieForm(FlaskForm):
    rating = FloatField("Your Rating Out of 10 e.g. 7.5", validators=[DataRequired()])
    review = StringField("Your Review", validators=[DataRequired()])
    submit = SubmitField("Done")


class SearchMovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')


@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    all_movies = result.scalars().all()

    for i, movie in enumerate(all_movies):
        movie.ranking = len(all_movies) - i

    db.session.commit()

    return render_template("index.html", movies=all_movies)

@app.route("/edit", methods=['GET', 'POST'])
def rate_movie():
    movie_id: int = request.args.get('id')
    form = RateMovieForm()
    movie_to_update: object = db.get_or_404(Movie, movie_id)

    if request.method == 'POST':
        if form.validate_on_submit():
            movie_to_update.rating = float(form.rating.data)
            movie_to_update.review = form.review.data
            db.session.commit()
            return redirect(url_for('home'))

    return render_template('edit.html', form=form, movie=movie_to_update)


@app.route("/delete", methods=['GET', 'POST'])
def delete_movie():
    movie_id: int = request.args.get('id')
    movie_to_delete: object = db.get_or_404(Movie, movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/add', methods=['GET', 'POST'])
def add_movie():
    form = SearchMovieForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            movie_title: str = form.title.data
            api_url: str = "https://api.themoviedb.org/3/search/movie"
            response = requests.get(url=api_url, params={'api_key': API_KEY, 'query': movie_title})
            data = response.json()['results']
            return render_template('select.html', options=data)
    return render_template('add.html', form=form)


@app.route('/select')
def select_movie():
    movie_id: int = request.args.get('id')
    api_url: str = f'https://api.themoviedb.org/3/movie/{movie_id}'
    img_url: str = "https://image.tmdb.org/t/p/w500"
    response = requests.get(url=api_url, params={'api_key': API_KEY, 'language': 'en-US'})
    response.raise_for_status()
    data = response.json()

    
    new_movie = Movie(
        title=data['title'],
        img_url=f"{img_url}{data['poster_path']}",
        year=data['release_date'].split('-')[0],
        description=data['overview']
    )

    db.session.add(new_movie)
    db.session.commit()

    movie = db.session.execute(db.select(Movie).where(Movie.title == new_movie.title)).scalar()
    return redirect(url_for('rate_movie', id=movie.id))


if __name__ == '__main__':
    app.run(debug=True)
