import random
import pandas as pd
from tkinter import *
from const import *
from typing import List

# TODO: connect to googlesheet and add repetition mechanism
class FlashCard:

    def __init__(self):
        self.window: Tk = Tk()
        self.canvas: Canvas = Canvas(width=800, height=526)
        self.card_front_image: PhotoImage = PhotoImage(file="images/card_front.png")
        self.card_back_image: PhotoImage = PhotoImage(file="images/card_back.png")
        self.card_background = self.canvas.create_image(400, 263, image=self.card_front_image)
        self.card_title: str = self.canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
        self.card_word: str = self.canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))

        self.check_image: PhotoImage = PhotoImage(file="images/right.png")
        self.cross_image: PhotoImage = PhotoImage(file="images/wrong.png")
        self.known_button: Button = Button(image=self.check_image, highlightthickness=0)
        self.unknown_button: Button = Button(image=self.cross_image, highlightthickness=0)
        
        self.words_to_learn: List[dict] = self.load_data("data/word_to_learn.csv")
        self.current_card: dict = {}
        self.flip_timer = None

    def load_data(self, filename: str) -> List[dict]:
        try:
            data: pd.DataFrame = pd.read_csv(filename)
        except FileNotFoundError:
            data: pd.DataFrame = pd.read_csv(ORIGINAL_DATA)
        return data.to_dict(orient="records")

    def setup(self) -> None:
        self.window.title("Flashy")
        self.window.config(bg=BACKGROUND_COLOR)
        self.canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
        self.known_button.config(bg=BACKGROUND_COLOR, highlightbackground=BACKGROUND_COLOR)
        self.unknown_button.config(bg=BACKGROUND_COLOR, highlightbackground=BACKGROUND_COLOR)

    def next_card(self) -> None:
        if self.flip_timer:
            self.window.after_cancel(self.flip_timer)
        self.current_card = random.choice(self.words_to_learn)
        self.canvas.itemconfig(self.card_title, text="French", fill="black")
        self.canvas.itemconfig(self.card_word, text=self.current_card['French'], fill="black")
        self.canvas.itemconfig(self.card_background, image=self.card_front_image)
        self.flip_timer = self.window.after(3_000, self.flip_card)

    def is_known(self) -> None:
        self.words_to_learn.remove(self.current_card)
        data: pd.DataFrame = pd.DataFrame(self.words_to_learn)
        data.to_csv("data/words_to_learn.csv", index=False)
        self.next_card()

    def flip_card(self) -> None:
        self.canvas.itemconfig(self.card_title, text="English", fill="white")
        self.canvas.itemconfig(self.card_word, text=self.current_card['English'], fill="white")
        self.canvas.itemconfig(self.card_background, image=self.card_back_image)
    
    def buttons_add_command(self) -> None:
        self.known_button.config(command=self.is_known)
        self.unknown_button.config(command=self.next_card)

    def layout(self) -> None:
        self.window.config(padx=50, pady=50)
        self.canvas.grid(row=0, column=0, columnspan=2)
        self.unknown_button.grid(row=1, column=0)
        self.known_button.grid(row=1, column=1)
        
    def start(self) -> None:
        self.setup()
        self.buttons_add_command()
        self.layout()
        self.next_card()
        self.window.mainloop()

if __name__ == "__main__":
    app = FlashCard()
    app.start()