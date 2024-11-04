from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, SelectField
from wtforms.validators import DataRequired, URL
from typing import List
import csv
import pandas as pd

'''
On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), URL()])
    open = TimeField('Open', validators=[DataRequired()])
    close = TimeField('Close', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee', choices=['☕', '☕☕', '☕☕☕', '☕☕☕☕️', '☕☕☕☕️☕️'], validators=[DataRequired()])
    wifi_rating = SelectField('Wifi', choices=['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'], validators=[DataRequired()])
    power_rating = SelectField('Power', choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'], validators=[DataRequired()])
    submit = SubmitField('Submit')


class Cafe:
    @classmethod
    def to_list(cls, form: CafeForm) -> List[str]:
        new_cafe: List[str] = []
        new_cafe.append(form.cafe.data)
        new_cafe.append(form.location.data)
        new_cafe.append(form.open.data.strftime('%H:%M'))
        new_cafe.append(form.close.data.strftime('%H:%M'))
        new_cafe.append(form.coffee_rating.data)
        new_cafe.append(form.wifi_rating.data)
        new_cafe.append(form.power_rating.data)
        return new_cafe


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            df = pd.read_csv('cafe-data.csv')
            new_cafe_df = pd.DataFrame([Cafe.to_list(form)], columns=df.columns)
            df = pd.concat([df, new_cafe_df], ignore_index=True)
            df.to_csv('cafe-data.csv', index=False)
            return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
