import random
import smtplib
import datetime as dt
import pandas as pd

GMAIL = "YOUR-GMAIL@gmail.com" # Replaced it with your gamil address
GMAIL_PASSWORD = "YOUR-APP-PASSWORD" # Generate your gmail app password, and replace it.
HOSTS = {
    "gmail": "smtp.gmail.com", 
    "yahoo": "smtp.mail.yahoo.com",
    "hotmail": "smtp.live.com",
    "outlook": "smtp-mail.outlook.com"
}
PLACEHOLDER = "[NAME]"

# Update the birthdays.csv
data_df = pd.read_csv("birthdays.csv")
birthdays_dict = {(data_row.month, data_row.day): data_row for index, data_row in data_df.iterrows()}

# Check if today matches a birthday in the birthdays.csv
today = (dt.datetime.now().month, dt.datetime.now().day)

if today in birthdays_dict:
    # Pick a random letter from letter templates
    file_path = f"letter_templates/letter_{random.randint(1,3)}.txt"
    birthday_person = birthdays_dict[today]
    with open(file_path) as letter_file:
        contents = letter_file.read()
        # Replace the [NAME] with the person's actual name from birthdays.csv
        contents = contents.replace(PLACEHOLDER, birthday_person["name"])

    # Send the letter to that person's email address.
    with smtplib.SMTP(HOSTS["gmail"]) as connection:
        connection.starttls()
        connection.login(user=GMAIL, password=GMAIL_PASSWORD)
        connection.sendmail(
            from_addr=GMAIL,
            to_addrs=birthday_person["email"],
            msg=f"Subject:Happy Birthday\n\n{contents}"
        )
