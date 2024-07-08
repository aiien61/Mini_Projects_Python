import os
import turtle
import pandas as pd
from pathlib import Path
from typing import Set, List
from multiprocessing import Pool

IMAGE = "blank_states_img.gif"

class Game:
    screen: turtle.Screen = turtle.Screen()
    archive: str = "states_to_learn.csv"

    def __init__(self):
        self.data: pd.DataFrame = self.get_states_data()
        self.missing_states: List[str] = self.restore()
        self.setup()

    def setup(self) -> None:
        self.screen.title("U.S. States Game")
        self.screen.addshape(IMAGE)
        turtle.shape(IMAGE)

    def restore(self):
        if Path(self.archive).is_file():
            return pd.read_csv(self.archive).Unsolved_States.to_list()
        return self.data.state.to_list()

    def reset(self) -> bool:
        os.remove('states_to_learn.csv')
        return True

    def get_answer_state(self) -> str:
        title: str = f"{50 - len(self.missing_states)}/50 States Correct"
        answer_state = self.screen.textinput(title=title, prompt="What's another state's name?")
        return answer_state.title()
    
    def get_states_data(self) -> pd.DataFrame:
        data: pd.DataFrame = pd.read_csv("50_states.csv")
        return data
    
    def write_down_state_name(self, state: str) -> None:
        cursor = turtle.Turtle()
        cursor.hideturtle()
        cursor.penup()
        state_data: pd.DataFrame = self.data[self.data.state == state]
        cursor.goto(int(state_data.x), int(state_data.y))
        cursor.write(state_data.state.item())
        return None

    def play(self):
        all_states: Set[str] = set(self.data.state.to_list())
        missing_states: Set[str] = set(self.missing_states)
        if len(missing_states) != len(all_states):
            all_states.difference_update(missing_states)
            for state in all_states:
                self.write_down_state_name(state)

        while missing_states:
            answer_state = self.get_answer_state()
            if answer_state == "Exit":
                unsolved_states: List[str] = list(missing_states)
                pd.DataFrame({"Unsolved_States": unsolved_states}).to_csv(self.archive, index=False)
                break

            if answer_state in missing_states:
                missing_states.remove(answer_state)
                self.write_down_state_name(answer_state)

        self.screen.mainloop()
