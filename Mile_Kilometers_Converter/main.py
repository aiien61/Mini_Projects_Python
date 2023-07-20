from tkinter import *


def miles_to_km():
    miles = float(miles_input.get())
    km = round(miles * 1.609)
    kilometer_result_label.config(text=f"{km}")


window = Tk()
window.title("Miles to Km Converter")
window.config(padx=20, pady=20)

miles_input = Entry(width=7)
miles_input.grid(column=1, row=0)

kilometer_result_label = Label(text="0")
kilometer_result_label.grid(column=1, row=1)

calculate_button = Button(text="Calculate", command=miles_to_km)
calculate_button.grid(column=1, row=2)

labels = [
    {
        "text": "Miles",
        "column": 2,
        "row": 0
    },
    {
        "text": "is equal to",
        "column": 0,
        "row": 1
    },
    {
        "text": "Km",
        "column": 2,
        "row": 1
    }
]

for label in labels:
    Label(text=label["text"]).grid(column=label["column"], row=label["row"])

window.mainloop()
