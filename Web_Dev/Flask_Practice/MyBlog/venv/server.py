from flask import Flask, render_template
from datetime import datetime
import random
import requests

app = Flask(__name__)

@app.route('/')
def home():
    random_number: int = random.randint(0, 10)
    current_time = datetime.now()
    return render_template('index.html', num=random_number, year=current_time.year, name="Arrow")

@app.route('/guess/<name>')
def guess(name: str):
    age_api: str = "https://api.agify.io/"
    age_response = requests.get(url=age_api, params={"name": name})
    age_data = age_response.json()
    age = age_data['age']

    gender_api: str = "https://api.genderize.io/"
    gender_response = requests.get(url=gender_api, params={"name": name})
    gender_data = gender_response.json()
    gender = gender_data['gender']

    return render_template('guess.html', name=name, age=age, gender=gender)

@app.route('/blog/<num>')
def get_blog(num: int):
    print(num)
    blog_api: str = "https://api.npoint.io/c790b4d5cab58020d391"
    blog_response = requests.get(url=blog_api)
    all_posts = blog_response.json()
    return render_template("blog.html", all_posts=all_posts, num=num)

if __name__ == "__main__":
    app.run(debug=True)