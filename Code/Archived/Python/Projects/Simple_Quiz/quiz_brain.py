class QuizBrain:
    def __init__(self,q_list) -> None:
        self.question_number = 0
        self.question_list = q_list
        self.score = 0

    def next_question(self):
        current_question = self.question_list[self.question_number]
        self.question_number += 1
        user_answer = input(f"\nQ{self.question_number}. [Category:{current_question.category}][Difficulty:{current_question.difficulty}]: {current_question.text} [True/False] --> ")
        self.check_answer(user_answer,current_question.answer)

    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    def check_answer(self,user_answer,correct_answer):
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            print("You got it right.")
        else:
            print("You got it wrong.")
            print(f"The correct answer is {correct_answer}.")
        print(f"Your score is {self.score}.")

