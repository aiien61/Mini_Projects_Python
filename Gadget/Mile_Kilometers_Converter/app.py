from tkinter import *

class MileConverter:
    def __init__(self):
        self.window: Tk = Tk()
        self.miles_input: Entry = Entry(width=7)
        self.mile_label: Label = Label(text="Miles")
        self.is_equal_label: Label = Label(text="is equal to")
        self.kilometer_result_label: Label = Label(text="0")
        self.kilometer_label: Label = Label(text="Km")
        self.calculate_button: Button = Button(text="Calculate", command=self.miles_to_km)


    def setup(self):
        self.window.title("Miles to Km Converter")
        self.window.minsize(width=300, height=150)
        self.window.config(padx=20, pady=20, bg="white")
        self.miles_input.focus()
        self.miles_input.insert(END, string="0")

    def config_colors(self, bg: str, fg: str, highlightbackground: str) -> None:
        self.miles_input.config(bg=bg, fg=fg, highlightbackground=highlightbackground)
        self.mile_label.config(bg=bg, fg=fg, highlightbackground=highlightbackground)
        self.is_equal_label.config(bg=bg, fg=fg, highlightbackground=highlightbackground)
        self.kilometer_result_label.config(bg=bg, fg=fg, highlightbackground=highlightbackground)
        self.kilometer_label.config(bg=bg, fg=fg, highlightbackground=highlightbackground)
        self.calculate_button.config(bg=bg, fg=fg, highlightbackground=highlightbackground)
        return None
        

    def miles_to_km(self) -> None:
        miles: float = float(self.miles_input.get())
        km: float = miles * 1.609
        self.kilometer_result_label.config(text=str(km))
        return None

    def layout(self):
        # column0
        self.is_equal_label.grid(row=1, column=0)

        # column1
        self.miles_input.grid(row=0, column=1)
        self.kilometer_result_label.grid(row=1, column=1)
        self.calculate_button.grid(row=2, column=1)

        # column2
        self.mile_label.grid(row=0, column=2)
        self.kilometer_label.grid(row=1, column=2)


    def run(self):
        self.setup()
        self.config_colors(bg="white", fg="black", highlightbackground="white")
        self.layout()

        self.window.mainloop()

if __name__ == "__main__":
    converter: MileConverter = MileConverter()
    converter.run()