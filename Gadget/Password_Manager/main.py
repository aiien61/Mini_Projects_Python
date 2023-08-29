import json
import random
import string
from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle

import pyperclip

# ---------------------------- PASSWORD GENERATOR --------------------- #
def generate_password() -> None:
    letters = string.ascii_letters
    numbers = list(map(str, range(10)))
    symbols = string.punctuation

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    return None

# ---------------------------- SAVE PASSWORD -------------------------- #
def save() -> None:
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if (not website) or (not email) or (not password):
        messagebox.showinfo(
            title="Oops", message="Please don't leave any fields empty!")
    else:
        message = f"Email: {email} \nPassword: {password} \nIs it ok to save?"
        is_ok = messagebox.askokcancel(title=website, message=message)
    
        if is_ok:
            try:
                with open("data.json", mode='r') as f:
                    # Reading old data
                    data = json.load(f)
            except FileNotFoundError:
                # Creating a new file
                with open("data.json", mode='w') as f:
                    json.dump(new_data, f, indent=4)
            else:
                # Updating old data with new data
                data.update(new_data)
                
                with open("data.json", mode='w') as f:
                    # Saving updated data
                    json.dump(data, f, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)
    return None

# ---------------------------- SEARCH PASSWORD ------------------------ #
def search() -> None:
    website = website_entry.get()
    try:
        with open("data.json", mode='r') as f:
            data = json.load(f)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            message = f"Email: {email}\nPassword: {password}"
            messagebox.showinfo(title=website, message=message)
        else:
            message = f"No details for {website} exists."
            messagebox.showinfo(title="Error", message=message)
    return None

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.config(padx=50, pady=50)
window.title("Password Manager")

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries
website_entry = Entry(width=21)
website_entry.grid(column=1, row=1)
website_entry.focus()

email_entry = Entry(width=38)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, 'example@gmail.com')

password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)

# Buttons
search_button = Button(text="Search", width=13, command=search)
search_button.grid(column=2, row=1)

gen_pw_button = Button(text="Generate Password", command=generate_password)
gen_pw_button.grid(column=2, row=3)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
