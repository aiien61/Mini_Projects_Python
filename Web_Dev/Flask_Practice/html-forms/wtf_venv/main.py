from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap5

'''
On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt
'''

app = Flask(__name__)
app.secret_key = "something secret"

bootstrap = Bootstrap5(app)

class MyForm(FlaskForm):
    email = EmailField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField(label="Login", render_kw={"class": "btn btn-primary btn-lg"})

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = MyForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.email.data == 'admin@email.com' and form.password.data == '12345678':
                return render_template('success.html')
            else:
                return render_template('denied.html')
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
