from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import NotFound
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

# CREATE DATABASE
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['UPLOAD_FOLDER'] = 'static/files'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


# Configure Flask-Login's Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

# Create a login loader callback
@login_manager.user_loader
def load_user(user_id: int):
    return db.get_or_404(User, user_id)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data: dict = request.form
        hashed_and_salted_password = generate_password_hash(
            data.get('password'),
            method="pbkdf2:sha256", 
            salt_length=8
        )
        new_user = User(
            name=data.get('name'),
            email=data.get('email'),
            password=hashed_and_salted_password
        )
        if db.session.execute(db.select(User).where(User.email == new_user.email)).scalar():
            flash("You've already signed up with the email. Please log in instead.")
        else:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('secrets', user_id=new_user.id))
    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email: str = request.form.get("email")
        user = db.session.execute(db.select(User).where(User.email == user_email)).scalar()
        if user:
            if check_password_hash(user.password, request.form.get("password")):
                login_user(user)
                return redirect(url_for('secrets', user_id=user.id))
            else:
                flash("Incorrect password. Please try again.")
        else:
            flash("The email does not exist. Please try again.")

    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route('/secrets/<user_id>')
@login_required
def secrets(user_id: int):
    try:
        user = db.get_or_404(User, user_id)
        return render_template("secrets.html", name=user.name, logged_in=current_user.is_authenticated)
    except NotFound as e:
        return jsonify(error={'Forbidden': 'Sorry, the user is not found in the database.'})
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
@login_required
def download():
    try:
        filename: str = 'cheat_sheet.pdf'
        return send_from_directory(directory=app.config['UPLOAD_FOLDER'], path=filename, as_attachment=True)
    except NotFound as e:
        return jsonify(error={'message': 'The file is not found.'})



if __name__ == "__main__":
    app.run(debug=True)
