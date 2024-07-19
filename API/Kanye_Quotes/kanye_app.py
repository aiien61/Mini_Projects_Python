import requests
from tkinter import *


class KanyeApp:
    FONT = ("Arial", 30, "bold")

    def __init__(self):
        self.window: Tk = Tk()
        self.canvas: Canvas = Canvas(width=300, height=414)
        self.background_img: PhotoImage = PhotoImage(file="background.png")
        self.canvas.create_image(150, 207, image=self.background_img)
        self.quote_text = self.canvas.create_text(150, 207, text="")
        self.canvas.itemconfig(self.quote_text, width=250, font=self.FONT, fill="black")
        self.kanye_img: PhotoImage = PhotoImage(file="kanye.png")
        self.kanye_button: Button = Button(image=self.kanye_img, highlightthickness=0)

    def setting(self):
        self.window.title("Kanye Says...")
        self.window.config(background="white")
        self.canvas.config(background="white", highlightthickness=0)
        self.kanye_button.config(command=self.get_quote)
        

    def layout(self):
        self.window.config(padx=50, pady=50)
        self.canvas.grid(row=0, column=0)
        self.kanye_button.grid(row=1, column=0)


    def get_quote(self) -> None:
        response: requests.Response = requests.get(url="https://api.kanye.rest")
        response.raise_for_status()
        data: dict = response.json()
        quote: str = data["quote"]
        if len(quote) > 50:
            self.get_quote()
        self.canvas.itemconfig(self.quote_text, text=quote)
        return None


    def run(self):
        self.setting()
        self.layout()
        self.get_quote()
        self.window.mainloop()

if __name__ == "__main__":
    kanye = KanyeApp()
    kanye.run()
