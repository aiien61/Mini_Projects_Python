import pandas

data_df = pandas.read_csv("nato_phonetic_alphabet.csv")
phonetic_dict = {row.letter: row.code for index, row in data_df.iterrows()}

word = input("Enter a word: ").upper()
print([phonetic_dict[letter] for letter in word])

