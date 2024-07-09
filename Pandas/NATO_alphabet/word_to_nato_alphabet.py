import pandas as pd
from typing import List

df: pd.DataFrame = pd.read_csv("nato_phonetic_alphabet.csv")
phonetic_dict: dict = {row.letter: row.code for _, row in df.iterrows()}

def generate_phonetic() -> None:
    word: str = input("Enter a word: ").upper()
    if word == "EXIT":
        return None

    try:
        output_list: List[str] = [phonetic_dict[letter] for letter in word]
    except KeyError:
        print(f"Sorry, only letters in the alphabet please.")
    else:
        print(output_list)
    finally:
        generate_phonetic()

if __name__ == "__main__":
    generate_phonetic()
