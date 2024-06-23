import random
from typing import List
from data import question_data
from quiz_brain import QuizBrain
from question_model import QuestionNode, LinkedList, Answer

def play_quiz_game():
    choice: str = input('Choose difficulty? (y/n): ').lower()
    if choice == 'y':
        difficulty: str = input("easy / medium / hard ?: ").lower()
        question_pool: List[dict] = [question for question in question_data['results']
                                     if question['difficulty'] == difficulty]
    else:
        question_pool: List[dict] = question_data['results']
    
    question_bank: LinkedList = LinkedList()
    for question in random.sample(question_pool, 10):
        text: str = question['question']
        answer: Answer = Answer.TRUE if question['correct_answer'] == 'True' else Answer.FALSE
        new_question: QuestionNode = QuestionNode(text, answer)
        question_bank.append(new_question)

    quiz = QuizBrain(question_bank)
    while quiz.still_has_question():
        quiz.next_question()

    print("You've completed the quiz.")
    print(f"Your final score was: {quiz.score}/{quiz.question_number}")

if __name__ == '__main__':
    play_quiz_game()