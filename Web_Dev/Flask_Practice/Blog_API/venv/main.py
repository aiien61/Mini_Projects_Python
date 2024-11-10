from flask import Flask, render_template, redirect, url_for, jsonify, request
import werkzeug.exceptions
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date


'''
On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt
'''

ckeditor = CKEditor()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'blog-secret-key'
ckeditor.init_app(app)
Bootstrap5(app)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


class CreatePostForm(FlaskForm):
    title = StringField(label='Blog Post Title', validators=[DataRequired()])
    subtitle = StringField(label='Subtitle', validators=[DataRequired()])
    author = StringField(label="Your Name", validators=[DataRequired()])
    img_url = StringField(label="Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField(label="Blog Content", validators=[DataRequired()])
    submit = SubmitField(label="Submit Post")


with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)

@app.route('/post/<post_id>')
def show_post(post_id: int):
    try:
        requested_post = db.get_or_404(BlogPost, post_id)
        return render_template("post.html", post=requested_post)
    except werkzeug.exceptions.NotFound as e:
        return jsonify(error={"Forbidden": "Sorry, the post is not found in the database."})


@app.route('/new-post', methods=['POST', 'GET'])
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            author=form.author.data,
            img_url=form.img_url.data,
            body=form.body.data,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template("make-post.html", form=form)
    

@app.route('/edit-post/<post_id>', methods=['POST', 'GET'])
def edit_post(post_id: int):
    try:    
        post_to_update = db.get_or_404(BlogPost, post_id)
        edit_form = CreatePostForm(
            title=post_to_update.title,
            subtitle=post_to_update.subtitle,
            author=post_to_update.author,
            img_url=post_to_update.img_url,
            body=post_to_update.body
        )
        if edit_form.validate_on_submit():
            post_to_update.title = edit_form.title.data
            post_to_update.subtitle = edit_form.subtitle.data
            post_to_update.author = edit_form.author.data
            post_to_update.img_url = edit_form.img_url.data
            post_to_update.body = edit_form.body.data
            db.session.commit()
            return redirect(url_for('show_post', post_id=post_to_update.id))
        return render_template('make-post.html', form=edit_form, is_edit=True)
    except werkzeug.exceptions.NotFound as e:
        return jsonify(error={"Forbidden": "Sorry, the post is not found in the database."})

@app.route('/delete/<post_id>')
def delete_post(post_id: int):
    try:
        post_to_delete = db.get_or_404(BlogPost, post_id)
        db.session.delete(post_to_delete)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    except werkzeug.exceptions.NotFound as e:
        return jsonify(error={"Forbidden": "Sorry, the post is not found in the database."})

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
