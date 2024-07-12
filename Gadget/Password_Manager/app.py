import pyperclip
import string
from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
from typing import List

class PasswordManager:
    def __init__(self):
        self.window: Tk = Tk()
        self.window.title("Password Manager")
        self.logo_img: PhotoImage = PhotoImage(file="logo.png")
        self.canvas: Canvas = Canvas(width=200, height=200)
        self.canvas.create_image(100, 100, image=self.logo_img)
        
        self.website_label: Label = Label(text="Website:")
        self.email_label: Label = Label(text="Email/Username:")
        self.password_label: Label = Label(text="Password:")
        
        self.website_entry = Entry(width=38)
        self.email_entry = Entry(width=38)
        self.password_entry = Entry(width=21)

        self.generate_button = Button(text="Generate Password", command=self.generate_password)
        self.add_button = Button(text="Add", width=36, command=self.save)
        
    
    def setup(self):
        self.window.config(padx=50, pady=50)
        self.website_entry.focus()
        self.email_entry.insert(END, 'example@gmail.com')

    def layout(self):
        self.canvas.grid(row=0, column=1)

        self.website_label.grid(row=1, column=0)
        self.email_label.grid(row=2, column=0)
        self.password_label.grid(row=3, column=0)

        self.website_entry.grid(row=1, column=1, columnspan=2)
        self.email_entry.grid(row=2, column=1, columnspan=2)
        self.password_entry.grid(row=3, column=1)

        self.generate_button.grid(row=3, column=2)
        self.add_button.grid(row=4, column=1, columnspan=2)

    
    def generate_password(self) -> bool:
        letters = string.ascii_letters
        numbers = list(map(str, range(10)))
        symbols = string.punctuation

        password_letters: List[str] = [choice(letters) for _ in range(randint(8, 10))]
        password_symbols: List[str] = [choice(symbols) for _ in range(randint(2, 4))]
        password_numbers: List[str] = [choice(numbers) for _ in range(randint(2, 4))]

        password_list: List[str] = password_letters + password_symbols + password_numbers
        shuffle(password_list)

        password: str = "".join(password_list)
        self.password_entry.insert(0, password)
        pyperclip.copy(password)
        return True

    def save(self) -> bool:
        website: str = self.website_entry.get()
        email: str = self.email_entry.get()
        password: str = self.password_entry.get()

        if len(website) == 0 or len(password) == 0:
            messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
        else:
            message: str = f"Email: {email} \nPassword: {password} \nIs it ok to save?"
            is_ok: bool = messagebox.askokcancel(title=website, message=message)
            if is_ok:
                with open('data.txt', 'a') as file:
                    file.write(f"{website} | {email} | {password}\n")
                    self.website_entry.delete(0, END)
                    self.password_entry.delete(0, END)
        return True
        
    def run(self):
        self.setup()
        self.layout()
        self.window.mainloop()

if __name__ == "__main__":
    app = PasswordManager()
    app.run()
