from flask import Flask, render_template
from typing import List
import requests


app = Flask(__name__)

response = requests.get(url="https://api.npoint.io/eec9dfcd76363a082dd4")
posts: List[dict] = response.json()

@app.route('/')
def home():
    return render_template('index.html', posts=posts)

@app.route('/post/<index>')
def get_post(index: str):
    for post in posts:
        if str(post['id']) == index:
            return render_template('post.html', post=post)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)