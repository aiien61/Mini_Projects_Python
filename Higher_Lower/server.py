import random
from flask import Flask

app = Flask(__name__)

HOME_GIF = "https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif"
HIGH_GIF = "https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif"
LOW_GIF = "https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif"
CORRECT_GIF = "https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif"

random_number = random.randint(0, 9)
print(random_number)


@app.route("/")
def home():
    return '<h1>Guess a number between 0 and 9</h1>' \
           f'<img src="{HOME_GIF}" />'


@app.route("/<int:number>")
def guess(number):
    if number > random_number:
        return '<h1 style="color: purple">Too high, try again!</h1>' \
               f'<img src="{HIGH_GIF}" />'
    elif number < random_number:
        return '<h1 style="color: red">Too low, try again!</h1>' \
               f'<img src="{LOW_GIF}" />'
    else:
        return '<h1 style="color: green">You found me!</h1>' \
               f'<img src="{CORRECT_GIF}" />'
    

if __name__ == "__main__":
    app.run(debug=True)
