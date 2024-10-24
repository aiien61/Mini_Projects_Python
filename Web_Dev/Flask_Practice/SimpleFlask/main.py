from flask import Flask
from dataclasses import dataclass

app = Flask(__name__)

def make_bold(function):
    def wrapper():
        return f"<b>{function()}</b>"
    return wrapper


def make_emphasis(function):
    def wrapper():
        return f"<em>{function()}</em>"
    return wrapper


def make_underlined(function):
    def wrapper():
        return f"<u>{function()}</u>"
    return wrapper


@app.route('/')
def hello_world():
    return '<h1 style="text-align: center">hello, world!</h1>' \
           '<p>This is a paragraph.</p>' \
           '<img src="https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif?cid=790b7611hpb2wso0gpzwg5by8w8pcjyto58lfsa86oewletv&ep=v1_gifs_search&rid=giphy.gif&ct=g" width=200px>'

@app.route('/bye')
@make_bold
@make_emphasis
@make_underlined
def bye():
    return 'See ya!'

@app.route('/username/<name>')
def greet(name: str) -> str:
    return f"Hello there {name}!"

@app.route('/username/<name>/1')
def greet1(name: str) -> str:
    return f"Hello there {name}!"

@app.route('/username/<path:name>')
def greet2(name: str) -> str:
    return f"Hello folk {name}"

@app.route('/username/<name>/<int:age>')
def greet_age(name: str, age: int) -> str:
    return f"Hello {name}, {age} years old"


@dataclass
class User:
    name: str = None
    is_logged_in: bool = False


def is_authenticated_decorator(function):
    def wrapper(*args, **kwargs):
        if args:
            if args[0].is_logged_in:
                function(*args, **kwargs)

        if kwargs:
            if kwargs['user'].is_logged_in:
                function(*args, **kwargs)
    return wrapper


@is_authenticated_decorator
def create_blog_post(user):
    print(f"This is {user.name}'s new blog post.")


if __name__ == "__main__":
    new_user = User('Arrow')
    new_user.is_logged_in = True
    create_blog_post(user=new_user)
    
    app.run(debug=True)
    