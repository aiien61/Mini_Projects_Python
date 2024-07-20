import html
from question_model import LinkedList, Answer, QuestionNode


class QuizBrain:
    def __init__(self, question_list: LinkedList):
        self.question_number: int = 0
        self.score: int = 0
        self.question_list: LinkedList = question_list

    def next_question(self) -> None:
        self.question_number += 1
        current_question: QuestionNode = self.question_list.pop_first()
        question_text: str = html.unescape(current_question.text)
        user_answer: str = input(f"Q.{self.question_number}: {question_text} (True/False): ")
        self.check_answer(user_answer, current_question.answer)
        return None

    def still_has_question(self) -> bool:
        return False if self.question_list.length == 0 else True

    def check_answer(self, user_answer: str, correct_answer: Answer) -> bool:
        user_answer = Answer.TRUE if user_answer.lower() == 'true' else Answer.FALSE
        if user_answer == correct_answer:
            self.score += 1
            print('You got it right!')
        else:
            print("That's wrong.")
        print(f"The correct answer was: {correct_answer.name}")
        print(f"Your current score is: {self.score}/{self.question_number}\n")
