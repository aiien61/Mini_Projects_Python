import requests, datetime
from flask import Flask, render_template

app = Flask(__name__)

posts = requests.get(url="https://api.npoint.io/63c37f8dcb409044f216").json()
today = datetime.datetime.now()
today_year = today.year
today_date = today.date().strftime('%B %d')

for post in posts:
    post['author'] = "Smith Cooper"
    post['date'] = f"{today_date}, {today_year}"
    post['img_url'] = "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80"


@app.route("/")
def index():
    return render_template("index.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/post/<int:post_id>")
def get_post(post_id: int):
    if len(posts) < id:
        return index()

    for post in posts:
        if post["id"] == post_id:
            return render_template("post.html", post=post)


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port="5000")
