import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///book-collection.db"

db.init_app(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float)

    def __repr__(self):
        return f"<Book {self.title}>"

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    with app.app_context():
        result = db.session.execute(db.select(Book).order_by(Book.id))
        all_books = result.scalars().all()
        print(all_books)
        return render_template('index.html', all_books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        book_data = request.form.to_dict()
        with app.app_context():
            new_book = Book(**book_data)
            db.session.add(new_book)
            db.session.commit()
        return redirect(url_for('home'))

    return render_template('add.html')


@app.route("/edit", methods=["GET", "POST"])
def edit():
    with app.app_context():
        if request.method == "POST":
            book_to_update = db.get_or_404(Book, request.form['id'])
            book_to_update.rating = request.form['rating']
            db.session.commit()
            return redirect(url_for('home'))
        
        book_selected = db.get_or_404(Book, request.args.get('id'))
        return render_template('edit_rating.html', book=book_selected)
    

@app.route('/delete')
def delete():
    with app.app_context():
        book_to_delete = db.get_or_404(Book, request.args.get('id'))
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

