import datetime
import requests
from flask import Flask, render_template
from post import Post, Post_List

app = Flask(__name__)

year = datetime.datetime.now().year

posts = requests.get(url="https://api.npoint.io/c790b4d5cab58020d391").json()
post_objects = Post_List(posts)


@app.route('/')
def home():
    return render_template("index.html", posts=post_objects, year=year)


@app.route("/post/<int:index>")
def show_post(index: int):
    if index > len(post_objects):
        return home()

    request_post = post_objects[index]
    return render_template("post.html", post=request_post)



if __name__ == "__main__":
    app.run(debug=True)
