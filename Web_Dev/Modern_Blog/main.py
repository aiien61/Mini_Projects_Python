import datetime
import requests
import smtplib
from flask import Flask, render_template, request

app = Flask(__name__)

# Replaced it with your gamil address
GMAIL = "YOUR-GMAIL@gmail.com"
# Generate your gmail app password, and replace it.
GMAIL_PASSWORD = "YOUR-APP-PASSWORD"
HOSTS = {
    "gmail": "smtp.gmail.com",
    "yahoo": "smtp.mail.yahoo.com",
    "hotmail": "smtp.live.com",
    "outlook": "smtp-mail.outlook.com"
}

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


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        for k, v in request.form.items():
            print(f"{k.title()}: {v}")
        send_mail(**request.form)
        msg="Successfully sent your message"
        return show_info(data=request.form, msg=msg)
    return render_template("contact.html")


@app.route("/post/<int:post_id>")
def get_post(post_id: int):
    if len(posts) < id:
        return index()

    for post in posts:
        if post["id"] == post_id:
            return render_template("post.html", post=post)


@app.route("/info")
def show_info(data: dict, msg: str):
    return render_template("info.html", data=data, msg=msg)


def send_mail(**kwargs):
    email_message = "\n".join([f"{k.title()}: {v}" for k, v in kwargs.items()])
    with smtplib.SMTP(HOSTS["gmail"]) as connection:
        connection.starttls()
        connection.login(user=GMAIL, password=GMAIL_PASSWORD)
        connection.sendmail(
            from_addr=GMAIL,
            to_addrs=GMAIL,
            msg=f"Subject:New Message From {kwargs['name']}\n\n{email_message}"
        )


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port="5000")
