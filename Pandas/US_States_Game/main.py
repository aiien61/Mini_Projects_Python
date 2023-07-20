import turtle
import pandas as pd

screen = turtle.Screen()
screen.title("U.S. States Game")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

data = pd.read_csv("50_states.csv")
all_states = set(data.state.to_list())
guessed_states = []

while len(guessed_states) < len(all_states):
    correct_guess = f"{len(guessed_states)}/50 States Correct"
    guess_prompt = "What's another state's name?"
    answer_state = screen.textinput(title=correct_guess,
                                    prompt=guess_prompt).title()
    
    if answer_state == "Exit":
        missing_states = all_states - set(guessed_states)
        new_data = pd.DataFrame(missing_states)
        new_data.to_csv("states_to_learn.csv")
        break
   
    if answer_state in all_states:
        guessed_states.append(answer_state)
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        state_data = data[data.state == answer_state]
        t.goto(int(state_data.x), int(state_data.y))
        t.write(answer_state)

turtle.mainloop()
