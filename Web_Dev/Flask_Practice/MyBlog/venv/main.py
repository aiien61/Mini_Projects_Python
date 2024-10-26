from flask import Flask, render_template
from post import Post
from typing import List
import requests

app = Flask(__name__)

blog_api: str = "https://api.npoint.io/c790b4d5cab58020d391"
blog_response = requests.get(url=blog_api)
all_posts = blog_response.json()
post_objects: List[Post] = []
for post in all_posts:
    post_objects.append(Post(post['id'], post['title'], post['subtitle'], post['body']))


@app.route('/')
def home():
    return render_template("index.html", all_posts=post_objects)

@app.route('/post/<index>')
def get_post(index: str):
    target_post = None
    for post in post_objects:
        if post.id == int(index):
            print(post.body)
            target_post = post
    return render_template("post.html", post=target_post)

if __name__ == "__main__":
    app.run(debug=True)
