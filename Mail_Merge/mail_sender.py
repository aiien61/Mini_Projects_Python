from pathlib import Path
from typing import List

class MailSender:
    PLACEHOLDER = "[name]"

    def __init__(self):
        self.receiver_names_file: str = None
        self.sample_letter_file: str = None
        self.mailbox_to_send: str = None

    def get_all_receiver_names(self) -> List[str]:
        with open(self.receiver_names_file) as names_file:
            names: List[str] = names_file.readlines()
        return names
    
    def get_sample_letter(self) -> str:
        with open(self.sample_letter_file) as letter_file:
            sample_letter: str = letter_file.read()
        return sample_letter
    
    def write_letter(self, receiver_name: str, sample_letter: str) -> str:
        new_letter: str = sample_letter.replace(self.PLACEHOLDER, receiver_name)
        return new_letter

    def send_letter(self) -> None:
        Path(self.mailbox_to_send).mkdir(parents=True, exist_ok=True)

        sample_letter: str = self.get_sample_letter()
        for receiver_name in self.get_all_receiver_names():
            stripped_name: str = receiver_name.strip()
            new_letter: str = self.write_letter(stripped_name, sample_letter)
            with open(f"{self.mailbox_to_send}/letter_for_{stripped_name}.txt", mode="w") as mail:
                mail.write(new_letter)

if __name__ == "__main__":
    mail_sender = MailSender()
    mail_sender.receiver_names_file = "Input/Names/invited_names.txt"
    mail_sender.sample_letter_file = "Input/Letters/starting_letter.txt"
    mail_sender.mailbox_to_send = "Output/LettersToSend"
    mail_sender.send_letter()