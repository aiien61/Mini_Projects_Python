from tkinter import *
from tkinter import messagebox

# ---------------------------- PASSWORD GENERATOR --------------------- #

# ---------------------------- SAVE PASSWORD -------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if (not website) or (not email) or (not password):
        message = "Please don't leave any fields empty!"
    else:
        message = f"These are the details entered: \nEmail: {email} \nPassword: {password} \nIs it ok to save?"
    
    is_ok = messagebox.askokcancel(title=website, message=message)
    
    if is_ok:
        with open("data.text", mode='a') as f:
            f.write(f"{website} | {email} | {password}\n")
            website_entry.delete(0, END)
            password_entry.delete(0, END)


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
website_entry = Entry(width=35)
website_entry.grid(column=1, row=1, columnspan=2)
website_entry.focus()

email_entry = Entry(width=35)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, 'example@gmail.com')

password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)

# Buttons
gen_pw_button = Button(text="Generate Password")
gen_pw_button.grid(column=2, row=3)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
