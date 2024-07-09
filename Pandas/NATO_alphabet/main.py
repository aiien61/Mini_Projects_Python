import pandas

DATA_DF = pandas.read_csv("nato_phonetic_alphabet.csv")
PHONETIC_DICT = {row.letter: row.code for index, row in DATA_DF.iterrows()}

def generate_phonetic():
    word = input("Enter a word: ").upper()
    try:
        output_list = [PHONETIC_DICT[letter] for letter in word]
    except KeyError:
        print(f"Sorry, only letters in teh alphabet please.")
    else:
        print(output_list)
    finally:
        generate_phonetic()


if __name__ == "__main__":
    generate_phonetic()
