import random
import requests
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

AGIFY_ENDPOINT = "https://api.agify.io"
GENDERIZE_ENDPOINT = "https://api.genderize.io"

@app.route("/")
def home():
    random_number = random.randint(1, 10)
    year = datetime.now().year
    return render_template("index.html", num=random_number, year=year)

@app.route("/guess/<name>")
def guess(name: str):
    name = name.lower()
    parameters = {"name": name}

    age_response = requests.get(url=AGIFY_ENDPOINT, params=parameters)
    age = age_response.json()["age"]

    gender_response = requests.get(url=GENDERIZE_ENDPOINT, params=parameters)
    gender = gender_response.json()["gender"]

    context = {"name": name.title(), "age": age, "gender": gender}

    return render_template("guess.html", **context)

if __name__ == "__main__":
    app.run(debug=True)
