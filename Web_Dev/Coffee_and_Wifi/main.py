from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = 'GENERATE-YOUR-SECRET-KEY'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    url = StringField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    open_time = StringField('Opening Time e.g. 8AM', validators=[DataRequired()])
    close_time = StringField('Closing Time e.g. 5:30PM', validators=[DataRequired()])
    rate = SelectField('Coffee Rating', choices=[
                       "☕️", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"], validators=[DataRequired()])
    wifi = SelectField('Wifi Strength Rating', choices=[
                       "✘", "🛜", "🛜🛜", "🛜🛜🛜", "🛜🛜🛜🛜", "🛜🛜🛜🛜🛜"], validators=[DataRequired()])
    power = SelectField('Power Socket Availability', choices=[
                        "✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"], validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_row = []
        new_row.append(form.cafe.data.strip())
        new_row.append(form.url.data.strip())
        new_row.append(form.open_time.data.strip())
        new_row.append(form.close_time.data.strip())
        new_row.append(form.rate.data.strip())
        new_row.append(form.wifi.data.strip())
        new_row.append(form.power.data.strip())
        print(new_row)

        with open('cafe-data.csv', mode='a', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(new_row)
        
        return redirect(url_for('cafes'))

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
