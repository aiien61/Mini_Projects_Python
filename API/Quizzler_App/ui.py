from tkinter import *
from quiz_brain import QuizBrain
from question_model import Answer

class QuizInterface:
    THEME_COLOR = "#375362"
    FONT = ("Arial", 20, "italic")
    next_question: str
    question_answer: Answer
    
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz: QuizBrain = quiz_brain
        self.window: Tk = Tk()
        self.score_label: Label = Label(text="Score: 0")
        self.canvas: Canvas = Canvas(width=300, height=250, highlightthickness=0)
        self.question_text: Text = self.canvas.create_text(150, 125, width=280, text="")
        self.true_image: PhotoImage = PhotoImage(file="images/true.png")
        self.true_button: Button = Button(image=self.true_image, command=self.true_pressed)
        self.false_image: PhotoImage = PhotoImage(file="images/false.png")
        self.false_button: Button = Button(image=self.false_image, command=self.false_pressed)
        
    def setup(self):
        self.window.title("Quizzler")
        self.window.config(bg=self.THEME_COLOR)
        self.score_label.config(fg="white", bg=self.THEME_COLOR, highlightthickness=0)
        self.canvas.itemconfig(self.question_text, fill=self.THEME_COLOR, font=self.FONT)
        self.true_button.config(highlightthickness=0)
        self.false_button.config(highlightthickness=0)

    def layout(self):
        self.window.config(padx=20, pady=20)
        self.score_label.grid(row=0, column=1)
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)
        self.true_button.grid(row=2, column=1)
        self.false_button.grid(row=2, column=0)

    def run(self):
        self.setup()
        self.layout()
        self.get_next_question()
        self.window.mainloop()


    def get_next_question(self) -> str:
        self.canvas.config(bg="white")
        self.canvas.itemconfig(self.question_text, fill=self.THEME_COLOR)
        if self.quiz.still_has_question():
            self.score_label.config(text=f"Score: {self.quiz.score}")
            self.next_question, self.question_answer = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=self.next_question)
        else:
            self.canvas.itemconfig(self.question_text, text="You've reached the end of the quiz.")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

    def true_pressed(self):
        is_right: bool = self.quiz.check_answer("True", self.question_answer)
        self.give_feedback(is_right)
        

    def false_pressed(self):
        is_right: bool = self.quiz.check_answer("False", self.question_answer)
        self.give_feedback(is_right)


    def give_feedback(self, is_right: bool):
        self.canvas.itemconfig(self.question_text, fill="white")
        if is_right:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")

        self.window.after(1_000, self.get_next_question)
