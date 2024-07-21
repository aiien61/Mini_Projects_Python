import random
from typing import List
from ui import QuizInterface
from data import question_data
from quiz_brain import QuizBrain
from question_model import QuestionNode, LinkedList, Answer


def play_quiz_game():
    question_pool: List[dict] = question_data['results']
    question_bank: LinkedList = LinkedList()
    for question in random.sample(question_pool, 10):
        text: str = question['question']
        answer: Answer = Answer.TRUE if question['correct_answer'] == 'True' else Answer.FALSE
        new_question: QuestionNode = QuestionNode(text, answer)
        question_bank.append(new_question)

    quiz = QuizBrain(question_bank)
    quiz_ui = QuizInterface(quiz)
    quiz_ui.run()


if __name__ == '__main__':
    play_quiz_game()
