from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def receive_data():
    if request.method == 'POST':
        username: str = request.form['username']
        password: str = request.form['password']
        return f"💪 Success! Form submitted. <h1>Name:{username} | Password: {password} <h1>"
    elif request.method == 'GET':
        return None


if __name__ == '__main__':
    app.run(debug=True)