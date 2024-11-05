from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from wtforms import SelectField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Dict, List

'''
On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt
'''

# Create the database class
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
db_name: str = 'book-collection.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'

# initialise the app with the extension
db.init_app(app)

# Define Models
class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self):
        return f'{self.title} - {self.author} - {self.rating}'

# Create tables according to defined table schema
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    all_books: List[object] = []
    with app.app_context():
        all_books = db.session.execute(db.select(Book).order_by(Book.title)).scalars().all()

    return render_template('index.html', books=all_books)


@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == 'POST':

        new_book = Book(
            title=request.form['title'],
            author=request.form['author'],
            rating=request.form['rating']
        )

        all_books = db.session.execute(db.select(Book)).scalars()
        if new_book.title not in [book.title for book in all_books]:
            db.session.add(new_book)
            db.session.commit()
            
        return redirect(url_for('home'))
    return render_template('add.html')

# TODO: use flask form select_field on book rating selection
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        book_id = request.form['id']
        print('book id: ', book_id)
        book = db.get_or_404(Book, book_id)
        book.rating = request.form['rating']
        db.session.commit()
        return redirect(url_for('home'))
    
    book_id: int = request.args.get('id')
    book_selected = db.get_or_404(Book, book_id)
    return render_template('edit_rating.html', book=book_selected)
        

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    book_id: int = request.args.get('id')
    book_to_delete = db.get_or_404(Book, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True)

