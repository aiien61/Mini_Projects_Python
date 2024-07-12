from tkinter import *

# ---------------------------- CONSTANTS ------------------------------ #
PINK: str = "#e2979c"
RED: str = "#e7305b"
GREEN: str = "#9bdeac"
YELLOW: str = "#f7f5dd"
FONT_NAME: str = "Courier"
WORK_MIN: int = 25
SHORT_BREAK_MIN: int = 5
LONG_BREAK_MIN: int = 20
CHECK_MARK: str = "✔"


class Pomodoro:
    repetition: int = 0
    timer: int | None = None

    def __init__(self):
        self.window: Tk = Tk()
        self.title_label: Label = Label(text="Timer")
        self.checkmark_label: Label = Label()
        self.start_button: Button = Button(text="Start", command=self.start_timer)
        self.reset_button: Button = Button(text="Reset", command=self.reset_timer)
        self.tomato_img: PhotoImage = PhotoImage(file="tomato.png")
        self.canvas: Canvas = Canvas(width=200, height=224)
        self.canvas.create_image(100, 112, image=self.tomato_img)
        self.timer_text = self.canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))

    def setup(self):
        self.window.title("Pomodoro")
        self.window.config(padx=100, pady=50, bg=YELLOW)
        self.canvas.config(bg=YELLOW, highlightthickness=0)
        self.title_label.config(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50, "bold"))
        self.checkmark_label.config(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 20, "bold"))
        self.start_button.config(fg="black", bg=YELLOW, highlightthickness=0, highlightbackground=YELLOW)
        self.reset_button.config(fg="black", bg=YELLOW, highlightthickness=0, highlightbackground=YELLOW)

    def layout(self):
        self.title_label.grid(row=0, column=1)
        self.checkmark_label.grid(row=3, column=1)
        self.start_button.grid(row=2, column=0)
        self.reset_button.grid(row=2, column=2)
        self.canvas.grid(column=1, row=1)

    def start_timer(self):
        self.repetition += 1

        work_seconds: int = WORK_MIN * 60
        short_break_seconds: int = SHORT_BREAK_MIN * 60
        long_break_seconds: int = LONG_BREAK_MIN * 60
        
        if self.repetition % 8 == 0:
            self.count_down(long_break_seconds)
            self.title_label.config(text="Break", fg=RED)
        elif self.repetition % 2 == 0:
            self.count_down(short_break_seconds)
            self.title_label.config(text="Break", fg=PINK)
        else:
            self.count_down(work_seconds)
            self.title_label.config(text="Work", fg=GREEN)

    def reset_timer(self):
        self.window.after_cancel(self.timer)
        self.repetition = 0
        self.title_label.config(text="Timer")
        self.checkmark_label.config(text="")
        self.canvas.itemconfig(self.timer_text, text="00:00")

    def count_down(self, count):
        self.canvas.itemconfig(self.timer_text, text=f"{count // 60:02d}:{count % 60:02d}")
        if count > 0:
            self.timer = self.window.after(1_000, self.count_down, count - 1)
        else:
            self.start_timer()
            marks = ""
            work_sessions: int = self.repetition // 2 
            marks += CHECK_MARK * work_sessions
            self.checkmark_label.config(text=marks)

    def run(self):
        self.setup()
        self.layout()
        self.window.mainloop()

if __name__ == "__main__":
    pomodoro = Pomodoro()
    pomodoro.run()