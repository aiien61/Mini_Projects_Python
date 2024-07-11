from tkinter import *

window: object = Tk()
window.title("My First GUI Program")
window.minsize(width=500, height=300)
window.config(background="white", padx=100, pady=200)

# Label
label: object = Label(text="I Am a Label", font=("Arial", 24, "bold"), bg="white", fg="black")
label.grid(column=0, row=0)
label.config(padx=50, pady=50)

# label['text'] = 'New Text'
# label.config(text='New Text')

# Button
def button_clicked():
    print("I got clicked")
    new_text = input.get()
    label.config(text=new_text)


button: object = Button(text='Click Me', command=button_clicked)
button.config(bg="white", fg="black", highlightbackground="white")
button.grid(column=1, row=1)

new_button: object = Button(text="New Button", command=button_clicked)
new_button.config(bg="white", fg="black", highlightbackground="white")
new_button.grid(column=2, row=0)

# Entry
entry: object = Entry(width=10)
entry.config(fg="black", bg="white", highlightbackground="white")
entry.insert(END, string="Some text to begin with")
entry.grid(column=3, row=2)


# Text
text: object = Text(height=5, width=30)
text.config(fg="black", bg="white", highlightbackground="white")
text.focus()
text.insert(END, "Example of multi-line text entry.")
print(text.get("1.0", END))
text.grid(column=2, row=2)

# Spinbox
def spinbox_used():
    print(spinbox.get())

spinbox: object = Spinbox(from_=0, to=10, width=5, command=spinbox_used)
spinbox.config(fg="black", bg="white", highlightbackground="white")
spinbox.grid(column=3, row=1)

# Scale
def scale_used(value):
    print(value)

scale: object = Scale(from_=0, to=100, command=scale_used)
scale.config(fg="black", bg="white", highlightbackground="white")
scale.grid(column=0, row=2)

# Checkbutton
def checkbutton_used():
    print(check_state.get())

check_state: object = IntVar()
check_button: object = Checkbutton(text="Is On?", variable=check_state, command=checkbutton_used)
check_button.config(fg="black", bg="white", highlightbackground="white")
check_button.grid(column=0, row=1)

# Radiobutton
def radio_used():
    print(radio_state.get())

radio_state: object = IntVar()
radio_button1 = Radiobutton(text="Option 1", value=1, variable=radio_state, command=radio_used)
radio_button2 = Radiobutton(text="Option 2", value=2, variable=radio_state, command=radio_used)
radio_button1.config(fg="black", bg="white", highlightbackground="white")
radio_button2.config(fg="black", bg="white", highlightbackground="white")
radio_button1.grid(column=1, row=0)
radio_button2.grid(column=1, row=1)

# Listbox
def listbox_used(event):
    print(Listbox.get(Listbox.curselection()))

listbox: object = Listbox(height=4)
listbox.config(fg="black", bg="white", highlightbackground="white")
fruits = ["Apple", "Pear", "Orange", "Banana"]
for item in fruits:
    listbox.insert(fruits.index(item), item)
listbox.bind("<<ListboxSelect>>", listbox_used)
listbox.grid(column=1, row=2)


window.mainloop()
