import json
import pyperclip
import string
from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
from typing import List, Iterable

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
        
        self.website_entry: Entry = Entry(width=21)
        self.email_entry: Entry = Entry(width=38)
        self.password_entry: Entry = Entry(width=21)

        self.generate_button: Button = Button(text="Generate", width=13, command=self.generate_password)
        self.add_button: Button = Button(text="Add", width=36, command=self.save)
        self.search_button: Button = Button(text="Search", width=13, command=self.search)
        
    
    def setup(self):
        self.window.config(padx=50, pady=50)
        self.website_entry.focus()
        self.email_entry.insert(END, 'example@gmail.com')

    def layout(self):
        self.canvas.grid(row=0, column=1)

        self.website_label.grid(row=1, column=0)
        self.email_label.grid(row=2, column=0)
        self.password_label.grid(row=3, column=0)

        self.website_entry.grid(row=1, column=1)
        self.email_entry.grid(row=2, column=1, columnspan=2)
        self.password_entry.grid(row=3, column=1)

        self.generate_button.grid(row=3, column=2)
        self.add_button.grid(row=4, column=1, columnspan=2)
        self.search_button.grid(row=1, column=2)

    
    def generate_password(self) -> bool:
        letters: Iterable[str] = string.ascii_letters
        numbers: List[str] = list(map(str, range(10)))
        symbols: Iterable[str] = string.punctuation

        password_letters: List[str] = [choice(letters) for _ in range(randint(8, 10))]
        password_symbols: List[str] = [choice(symbols) for _ in range(randint(2, 4))]
        password_numbers: List[str] = [choice(numbers) for _ in range(randint(2, 4))]

        password_list: List[str] = password_letters + password_symbols + password_numbers
        shuffle(password_list)

        password: str = "".join(password_list)
        self.password_entry.insert(0, password)
        pyperclip.copy(password)
        return True


    def search(self):
        website: str = self.website_entry.get().lower()
        try:
            data: dict = self.load_data(filename='data.json')
            website_data: dict = data[website]
            title: str = website
        except FileNotFoundError:
            title: str = "Error"
            message: str = "No Data File Found."
        except KeyError:
            title: str = "Error"
            message: str = f"No details for {website} exists."
        else:
            email: str = website_data['email']
            password: str = website_data['password']
            message: str = f"Email: {email}\nPassword: {password}"
        finally:
            messagebox.showinfo(title=title, message=message)
        

    def save(self) -> bool:
        website: str = self.website_entry.get().lower()
        email: str = self.email_entry.get()
        password: str = self.password_entry.get()
        
        new_data: dict = {
            website: {
                'email': email,
                'password': password
            }
        }

        if len(website) == 0 or len(password) == 0:
            messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
        else:
            try:
                # Reading old data
                data: dict = self.load_data(filename='data.json')
            
            except FileNotFoundError:
                # Creating a new file
                self.create_data(filename='data.json', data=new_data)
            
            else:
                # Updating old data with new data
                data.update(new_data)

                # Saving updated data
                self.write_to_file(filename='data.json', data=data)
            
            finally:
                self.website_entry.delete(0, END)
                self.password_entry.delete(0, END)
        return True
    

    def load_data(self, filename: str) -> dict:
        with open(filename, 'r') as file:
            return json.load(file)


    def create_data(self, filename: str, data: dict) -> None:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        return None


    def write_to_file(self, filename: str, data: dict) -> None:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        return None


    def run(self):
        self.setup()
        self.layout()
        self.window.mainloop()


if __name__ == "__main__":
    app = PasswordManager()
    app.run()
